# Dify Flex Message 整合故障排除指南

**日期**: 2026-04-22  
**版本**: 1.0  
**目的**: 記錄開發過程中碰到的常見問題和解決方案，避免未來重複踩坑

---

## 目錄

1. [LINE Flex Message 結構問題](#line-flex-message-結構問題)
2. [MySQL 資料庫導入問題](#mysql-資料庫導入問題)
3. [HeidiSQL 連接問題](#heidisql-連接問題)
4. [flex_api 返回值問題](#flex_api-返回值問題)

---

## LINE Flex Message 結構問題

### 問題 1: `contents` 欄位嵌套過深導致 LINE API 400 錯誤

**症狀**:
```
{
  "status_code": 400,
  "body": "{\"message\":\"A message (messages[0]) in the request body is invalid\",\"details\":[{\"message\":\"invalid property\",\"property\":\"/type\"}]}"
}
```

**根本原因**:
Dify 的 `assemble` 節點把 flex_api 返回的完整 Flex Message 又包裹了一層，導致結構變成：

```json
{
  "type": "flex",
  "altText": "...",
  "contents": {
    "type": "flex",      // ← 錯誤！不應該有第二層 type
    "altText": "...",
    "contents": {
      "type": "carousel",
      "contents": [...]
    }
  }
}
```

**正確結構**應該是：
```json
{
  "type": "flex",
  "altText": "...",
  "contents": {
    "type": "carousel",  // ← 直接是 carousel，不是 flex
    "contents": [...]
  }
}
```

**解決方案**:

1. **修改 flex_api 的返回值** (`flex-api/main.py`):
   ```python
   @app.get("/flex/{flex_id}", response_model=FlexOut)
   def get_flex(flex_id: str):
       with get_conn() as conn, conn.cursor() as cur:
           cur.execute(
               "SELECT id, description, contents FROM flex_message_templates WHERE id=%s",
               (flex_id,),
           )
           row = cur.fetchone()
       if not row:
           raise HTTPException(status_code=404, detail=f"flex_id '{flex_id}' not found")

       # 正規化 contents
       raw_contents = _normalize_contents(row["contents"])

       # 若 contents 是完整 Flex Message（type=flex），提取其 contents 欄位
       if isinstance(raw_contents, dict) and raw_contents.get("type") == "flex":
           row["contents"] = raw_contents.get("contents", raw_contents)
       else:
           row["contents"] = raw_contents

       return FlexOut(**row)
   ```

2. **修改 Dify workflow 的 assemble 節點**:
   ```python
   import json

   def main(fetch_body: str, status_code: int, description: str) -> dict:
       if status_code != 200:
           return {"messages_json": "", "error": "true", "error_msg": f"無資料: flex_id 不存在 (HTTP {status_code})"}

       try:
           parsed = json.loads(fetch_body)
       except Exception as e:
           return {"messages_json": "", "error": "true", "error_msg": f"無法解析模板: {e}"}

       # flex_api 現在返回 contents 物件（carousel, bubble 等），不包含外層 type=flex
       msg = {
           "type": "flex",
           "altText": description or "Flex Message",
           "contents": parsed["contents"] if isinstance(parsed, dict) and "contents" in parsed else parsed,
       }
       return {"messages_json": json.dumps([msg], ensure_ascii=False), "error": "false", "error_msg": ""}
   ```

---

## MySQL 資料庫導入問題

### 問題 2: JSON 中出現 `"additionalProp1"` 多包一層

**症狀**:
在 HeidiSQL 中查看 MySQL 表，`contents` 欄位顯示：
```json
{
  "additionalProp1": {
    "type": "flex",
    "altText": "...",
    "contents": {...}
  }
}
```

**根本原因**:
Pydantic 的 `response_model` 序列化時，會在某些情況下自動包裹物件，導致額外的層級。

**解決方案**:

在 HeidiSQL 中執行 SQL 修正：
```sql
UPDATE flex_message_templates 
SET contents = JSON_EXTRACT(contents, '$.additionalProp1')
WHERE id = 'cafe_dessert_showcase' 
AND JSON_CONTAINS(contents, JSON_OBJECT('additionalProp1', JSON_OBJECT()));
```

或刪除後重新插入正確的 JSON（**推薦**）：
```sql
DELETE FROM flex_message_templates WHERE id='cafe_dessert_showcase';

INSERT INTO flex_message_templates (id, description, contents) 
VALUES ('cafe_dessert_showcase', '咖啡與甜點推薦 5 選', 
'{"type":"carousel","contents":[...]}');
```

**預防方法**:
- 使用 HeidiSQL 等 GUI 工具直接插入，而不是複雜的 CLI 腳本
- 在 flex_api 中改用直接返回 dict，避免 Pydantic 序列化：
  ```python
  @app.get("/flex/{flex_id}")
  def get_flex(flex_id: str):
      # 返回純 dict，不用 response_model
      return {
          "id": row["id"],
          "description": row["description"],
          "contents": raw_contents
      }
  ```

---

## HeidiSQL 連接問題

### 問題 3: "Access denied for user 'root'@'192.168.0.1'"

**症狀**:
```
Access denied for user 'root'@'192.168.0.1' (using password: YES)
```

**根本原因**:
MySQL 容器只允許本地連接 (`127.0.0.1`)，不允許從區域網路 IP (`192.168.0.1`) 連接。

**解決方案**:

在 HeidiSQL 的連接設定中改為 `localhost` 而不是具體的 IP：

| 欄位 | 值 |
|------|---|
| **主機名稱** | `localhost` |
| **連接埠** | `13366` |
| **使用者** | `root` |
| **密碼** | `difyai123456` |

或者允許 MySQL 接受遠程連接：
```bash
docker exec docker-db_mysql-1 mysql -uroot -pdifyai123456 -e "
CREATE USER IF NOT EXISTS 'root'@'192.168.0.1' IDENTIFIED BY 'difyai123456';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'192.168.0.1' WITH GRANT OPTION;
FLUSH PRIVILEGES;
"
```

---

### 問題 4: "Public Key Retrieval is not allowed"

**症狀**:
```
Connection error: Public Key Retrieval is not allowed
```

**根本原因**:
MySQL 8.0 預設不允許公鑰檢索，這是安全設置。

**解決方案**:

在 HeidiSQL 的 **Advanced** 標籤中添加連接參數：

1. **點擊「Advanced」標籤**
2. 在「Driver properties」或連接參數中添加：
   ```
   allowPublicKeyRetrieval=true
   useSSL=false
   ```

或改 **URL** 欄位為：
```
jdbc:mysql://localhost:13366?allowPublicKeyRetrieval=true&useSSL=false
```

---

## flex_api 返回值問題

### 問題 5: flex_api 無法從區域網路 IP 連接 MySQL

**症狀**:
```
ERROR 2003 (HY000): Can't connect to MySQL server on '192.168.0.1:3306' (111)
```

**根本原因**:
Docker 容器內部與宿主機的網路是隔離的。容器無法看到宿主機的區域網路 IP。

**解決方案**:

在 Docker 容器內使用 `localhost` 或 `127.0.0.1` 連接 MySQL，而不是區域網路 IP。

在 flex_api 的環境變數中設置：
```yaml
environment:
  MYSQL_HOST: db_mysql    # Docker 內部 hostname，或 127.0.0.1
  MYSQL_PORT: 3306        # 容器內部 port，不是 13366
```

---

## 最佳實踐總結

### ✅ 正確的做法

1. **Flex Message 結構**:
   - 完整結構應該由 flex_api 返回，形如：
     ```json
     {
       "type": "carousel",  // 或 bubble
       "contents": [...]
     }
     ```
   - assemble 節點再包裝成完整的 Flex Message

2. **MySQL 導入**:
   - 使用 HeidiSQL GUI 直接插入和查看資料
   - 或用簡單的 SQL INSERT 語句
   - 避免複雜的 Python 腳本轉義

3. **HeidiSQL 連接**:
   - 優先用 `localhost` 而不是具體 IP
   - 連接參數加上 `allowPublicKeyRetrieval=true`

4. **Docker 內部連接**:
   - 容器間通信用 Docker hostname（如 `db_mysql`）
   - 不要用區域網路 IP

---

## 相關文檔

- [FLEX_MESSAGE_IMAGE_STORAGE.md](FLEX_MESSAGE_IMAGE_STORAGE.md) — 圖檔存放方案
- [REFACTOR_FLEX_MESSAGE.md](REFACTOR_FLEX_MESSAGE.md) — Flex Message 資料庫架構
- [DSL/Line_多選項連動助理_DB版.yml](DSL/Line_多選項連動助理_DB版.yml) — Dify workflow 定義
- [flex-api/main.py](flex-api/main.py) — FastAPI 服務程式碼

---

## 快速參考

### HeidiSQL 標準連接設定

```
連接名稱: dify_flex
網路類型: MariaDB or MySQL (TCP/IP)
主機名稱/IP: localhost
連接埠: 13366
使用者: root
密碼: difyai123456
資料庫: (連接後再選 line_flex)

[Advanced 標籤]
allowPublicKeyRetrieval=true
useSSL=false
```

### 檢查 MySQL 容器狀態

```bash
# 檢查容器是否運行
docker ps | grep mysql

# 檢查連接埠是否開放
netstat -an | grep 13366

# 用 root 帳號測試連接
docker exec docker-db_mysql-1 mysql -uroot -pdifyai123456 -e "SELECT 1;"
```

### 常用 SQL 命令

```sql
-- 查看所有模板
SELECT id, description, CHAR_LENGTH(contents) FROM flex_message_templates;

-- 查看特定模板
SELECT * FROM flex_message_templates WHERE id='cafe_dessert_showcase';

-- 驗證 contents 結構
SELECT JSON_EXTRACT(contents, '$.type') FROM flex_message_templates 
WHERE id='cafe_dessert_showcase';
```

---

## 版本歷史

| 版本 | 日期 | 內容 |
|------|------|------|
| 1.0 | 2026-04-22 | 初版 — 記錄 5 個主要問題和解決方案 |

