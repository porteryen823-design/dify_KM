# LINE Flex Message 重構文件

**日期**: 2026-04-21  
**版本**: 1.0  
**目標**: 將硬編碼在 DSL 裡的 Flex Message 模板遷移至 MySQL，建立 FastAPI 中介層，實現執行期動態模板切換

---

## 1. 概述

### 原狀態問題
- Flex Message JSON 硬編碼在 DSL workflow 的 http-request 節點 body（~400 行 raw-text）
- 新增模板必須修改並重新匯入 DSL
- 模板版本管理困難，無法與業務邏輯解耦
- 相同 workflow 邏輯被多個模板副本重複

### 新架構設計
```
LINE user
   │
   ▼  flex_id + query_message (start 節點輸入)
┌──────────────────────────────────────────┐
│ Dify workflow (advanced-chat)             │
│  start ─→ fetch_flex ─→ assemble ─→      │
│           send_line ─→ answer             │
└─────────┬──────────────────────────────────┘
          │ GET http://flex_api:8000/flex/{flex_id}
          ▼
┌──────────────────────────────────────────┐
│ flex_api (FastAPI, Docker service)       │
│  GET  /flex/{id}                          │
│  GET  /flex (list)                        │
│  POST /flex (upsert)                      │
│  DELETE /flex/{id}                        │
└─────────┬──────────────────────────────────┘
          │ pymysql + 内部 port 3306
          ▼
┌──────────────────────────────────────────┐
│ db_mysql (MySQL 8.0)                      │
│  外部 port: 13366                         │
│  DB: line_flex                            │
│  Table: flex_message_templates            │
└──────────────────────────────────────────┘
```

### 關鍵決策
- **資料來源**: FastAPI REST API（仿 leave-api / expense-api 既有慣例）
- **資料庫**: 新建獨立 MySQL DB `line_flex`，專屬 user `flex_api`（SELECT/INSERT/UPDATE/DELETE 權限）
- **部署**: flex_api service 整合進 docker-compose-template.yaml，自動生成 yaml 包含該服務
- **模板儲存**: JSON 物件儲存在 MySQL `flex_message_templates.contents` (JSON 欄位)
- **query_message 用途**: 作為 LINE Flex Message 的 `altText`（通知列顯示文字）

---

## 2. 實作清單

### 2.1 新建 flex-api FastAPI 服務

**位置**: `c:/VSCode_Proj/Dify/flex-api/`

#### 檔案結構
```
flex-api/
├── main.py                 # FastAPI 入點，3 個核心端點
├── requirements.txt        # 相依套件
├── Dockerfile              # Docker image 定義
├── .env.example            # 環境變數範例
├── README.md               # API 文件
└── sql/
    ├── init.sql            # DB / user / table / seed 初始化腳本
    ├── _generate_init.py   # 從原 DSL 抽取 JSON 生成 init.sql（一次性）
    ├── _seed_from_line_flex_message.py  # 從 LineFlexMessage 目錄掃描 JSON 並寫入 DB
    └── _verify.py          # 驗證 seed JSON 合法性
```

#### 核心 API 端點

| Method | Path          | 說明                                    | 回傳                      |
|--------|---------------|-----------------------------------------|--------------------------|
| GET    | `/`           | healthcheck                             | `{"status":"flex_api running"}` |
| GET    | `/flex`       | 列出所有模板 (id + description)         | `[{id, description}, ...]` |
| GET    | `/flex/{id}`  | 取得單一模板（完整 contents）           | `{id, description, contents}` |
| POST   | `/flex`       | 新增或覆蓋模板（upsert）                | `{id, description, contents}` |
| DELETE | `/flex/{id}`  | 刪除模板                                | `{deleted: id}`           |

#### 關鍵實作細節

**main.py** — `get_flex()` 端點：
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
    # MySQL JSON 型別返回時可能是字串，需反序列化
    row["contents"] = json.loads(row["contents"]) if isinstance(row["contents"], str) else row["contents"]
    return row
```

**核心優勢**:
- `contents` 回傳為 JSON 物件（dict），而非字串
- Dify workflow 的 code 節點可直接使用 `parsed["contents"]`，無需額外 JSON 解析

---

### 2.2 修改 docker-compose 配置

**修改檔案**: `dify/docker/docker-compose-template.yaml`

#### (a) db_mysql service 更新

```yaml
db_mysql:
  image: mysql:8.0
  profiles:
    - mysql
  restart: always
  environment:
    MYSQL_ROOT_PASSWORD: ${DB_PASSWORD:-difyai123456}
    MYSQL_DATABASE: ${DB_DATABASE:-dify}
  ports:
    - "${DB_MYSQL_HOST_PORT:-13366}:3306"  # ← 新增：宿主機 port 13366
  volumes:
    - ${MYSQL_HOST_VOLUME:-./volumes/mysql/data}:/var/lib/mysql
    - ../../flex-api/sql:/docker-entrypoint-initdb.d:ro  # ← 新增：啟動時執行 init.sql
  healthcheck:
    test: ["CMD", "mysqladmin", "ping", "-u", "root", "-p${DB_PASSWORD:-difyai123456}"]
    interval: 1s
    timeout: 3s
    retries: 30
```

#### (b) 新增 flex_api service

```yaml
flex_api:
  build:
    context: ../../flex-api
    dockerfile: Dockerfile
  profiles:
    - mysql
  restart: always
  environment:
    MYSQL_HOST: db_mysql
    MYSQL_PORT: 3306
    MYSQL_USER: ${FLEX_API_DB_USER:-flex_api}
    MYSQL_PASSWORD: ${FLEX_API_DB_PASSWORD:-flex_api_pwd_change_me}
    MYSQL_DATABASE: ${FLEX_API_DB_NAME:-line_flex}
  depends_on:
    db_mysql:
      condition: service_healthy
  ports:
    - "${FLEX_API_HOST_PORT:-8002}:8000"
```

#### 自動生成

修改 template 後需重新生成 `docker-compose.yaml`:
```bash
cd dify/docker
python generate_docker_compose
```

---

### 2.3 資料庫初始化腳本

**檔案**: `flex-api/sql/init.sql`

自動生成，包含：
1. 建立 `line_flex` 資料庫（utf8mb4 collation）
2. 建立 `flex_api` user（権限限制於 SELECT/INSERT/UPDATE/DELETE）
3. 建立 `flex_message_templates` 表
4. seed 資料（`all_elements_demo` + LineFlexMessage 目錄下的 4 個 JSON 檔）

#### 表結構

```sql
CREATE TABLE IF NOT EXISTS flex_message_templates (
  id           VARCHAR(64)  NOT NULL PRIMARY KEY,
  description  VARCHAR(255) NULL,
  contents     JSON         NOT NULL,
  created_at   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
  updated_at   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

| 欄位        | 類型           | 說明                                       |
|------------|----------------|-------------------------------------------|
| id         | VARCHAR(64)    | 模板識別碼（PK）                           |
| description| VARCHAR(255)   | 人類可讀描述（來自檔名或 altText）        |
| contents   | JSON           | Flex Message 的 `contents` 物件           |
| created_at | TIMESTAMP      | 建立時間                                   |
| updated_at | TIMESTAMP      | 更新時間（自動維護）                      |

---

### 2.4 資料遷移

#### 來源 1: 原 DSL 硬編碼

**工具**: `flex-api/sql/_generate_init.py`

- 從 `DSL/Line_多選項連動助理_涵蓋所有FLEX_MESSAGE功能.yml` 抽取 Flex Message contents
- 生成 init.sql 中的 seed 資料行（`all_elements_demo`）
- **執行**: `python _generate_init.py` → 生成 `init.sql`

#### 來源 2: LineFlexMessage 目錄 JSON 檔

**工具**: `flex-api/sql/_seed_from_line_flex_message.py`

掃描 `c:/VSCode_Proj/Dify/LineFlexMessage/*.json`，逐檔：
- 抽取 `contents` 物件（處理 3 種結構：直接 Flex、nested、陣列）
- id = 檔名（去 `.json`）
- description = 檔名或 altText（自動轉換，帶容錯）
- upsert 進 MySQL

**執行結果**:
```
[1] amazon_ai_brand_awareness.json
  [OK] Recovered from position 5085  (處理檔案損壞)
  [OK] Inserted/updated

[2] example.json
  [OK] Inserted/updated

[3] example_10張.json
  [OK] Inserted/updated

[4] example_涵蓋了 LINE Flex Message 的所有官方元素.json
  [OK] Inserted/updated
```

**總計**: 5 個模板已進 MySQL（原 1 個 + 新增 4 個）

---

### 2.5 重構 Dify workflow

**檔案**: `DSL/Line_多選項連動助理_DB版.yml`

#### 節點流程

```
start (輸入 flex_id + query_message)
  ↓
fetch_flex (HTTP GET /flex/{flex_id})
  ↓
assemble (Code: 組裝 LINE messages 陣列)
  ↓
send_line (HTTP POST 到 LINE API)
  ↓
answer (回覆用戶)
```

#### 節點詳解

**(1) start 節點**
- 變數 1: `flex_id` (text-input, required, max 64 chars)
- 變數 2: `query_message` (text-input, required, max 200 chars)

**(2) fetch_flex (HTTP GET)**
```yaml
url: http://flex_api:8000/flex/{{#start.flex_id#}}
method: get
timeout: 10s
```
- 輸出: `fetch_flex.body` (完整 JSON 字串，含 id/description/contents)

**(3) assemble (Code - Python3)**
```python
import json

def main(fetch_body: str, alt_text: str) -> dict:
    parsed = json.loads(fetch_body)
    msg = {
        "type": "flex",
        "altText": alt_text,
        "contents": parsed["contents"],
    }
    return {"messages_json": json.dumps([msg], ensure_ascii=False)}
```
- 輸入: `fetch_body` (HTTP 回應), `alt_text` (query_message)
- 輸出: `messages_json` (可直接塞進 POST body 的字串)

**為何要 code 節點?**
- LINE API 要求 contents 為 JSON 物件，不能是字串
- 若直接在 http-request raw-text 塞 `{{#fetch_flex.body#}}`，會被當字串嵌入造成結構錯誤
- code 節點確保 JSON 層級正確

**(4) send_line (HTTP POST)**
```yaml
url: https://api.line.me/v2/bot/message/push
method: post
headers:
  Authorization: Bearer {{#env.LINE_CHANNEL_ACCESS_TOKEN#}}
  Content-Type: application/json
body: |
  {
    "to": "{{#env.LINE_USER_ID#}}",
    "messages": {{#assemble.messages_json#}}
  }
```

**(5) answer 節點**
```
OK! 已發送 flex_id={{#start.flex_id#}} 至 LINE（status={{#send_line.status_code#}}）
```

---

## 3. 啟動與驗證

### 3.1 啟動服務

```bash
cd c:/VSCode_Proj/Dify/dify/docker

# 帶 mysql profile 啟動（包含 db_mysql + flex_api）
docker compose --profile mysql up -d --build db_mysql flex_api
```

### 3.2 初始化資料庫（若 volume 已存在）

MySQL 官方映像的 `/docker-entrypoint-initdb.d/` **只在 datadir 空時自動執行**。如果 `./volumes/mysql/data` 已有資料，需手動執行：

```bash
docker exec -i dify-db_mysql-1 mysql -uroot -pdifyai123456 < ../../flex-api/sql/init.sql
```

### 3.3 驗證資料庫

```bash
# 從宿主機透過 13366 port 連線
mysql -h 127.0.0.1 -P 13366 -u flex_api -p line_flex \
  -e "SELECT id, description FROM flex_message_templates;"

# 預期輸出：
# +------------------------------------+----------+
# | id                                 | description |
# +------------------------------------+----------+
# | all_elements_demo                  | Flex Message... |
# | amazon_ai_brand_awareness          | 【LINE 商家報 x amazon】... |
# | example                            | 商品推薦 |
# | example_10張                        | 10 張輪播卡片範例 |
# | example_涵蓋了...                    | Flex Message 完整功能展示 |
# +------------------------------------+----------+
```

### 3.4 驗證 API

```bash
# Health check
curl http://localhost:8002/
# {"status":"flex_api running"}

# 列表
curl http://localhost:8002/flex

# 取單一模板
curl http://localhost:8002/flex/amazon_ai_brand_awareness | python3 -m json.tool
```

### 3.5 驗證 Dify workflow

1. 進入 Dify web UI (`http://localhost:8080`)
2. 匯入 DSL 檔: `DSL/Line_多選項連動助理_DB版.yml`
3. workflow canvas 應顯示 5 個節點
4. 執行參數:
   - `flex_id`: `amazon_ai_brand_awareness`
   - `query_message`: `測試 Amazon AI 品牌意識`
5. 預期結果：
   - fetch_flex 返回 status 200
   - send_line 發送成功
   - 手機 LINE 收到訊息（通知列顯示 query_message）

---

## 4. 故障排除

### 4.1 flex_api 容器無法啟動

**症狀**: `docker compose ps` 看不到 flex_api

**原因**: docker-compose.yaml 未包含 flex_api service

**解決**:
```bash
cd dify/docker
python generate_docker_compose  # 重新生成
docker compose --profile mysql up -d --build flex_api
```

### 4.2 workflow 執行報 404

**症狀**: fetch_flex 回傳 "Request failed with status code 404"

**原因**: 
- flex_id 變數未正確傳入（輸入 `{}` 或空值）
- 或 flex_id 在 DB 中不存在

**解決**:
```bash
# 確認 flex_id 存在
curl http://localhost:8002/flex | grep flex_id

# 或指定完整 ID 重試
# flex_id: amazon_ai_brand_awareness
```

### 4.3 MySQL 連線失敗

**症狀**: flex_api 容器啟動但 app startup 失敗

**原因**: 
- db_mysql 未準備好（healthcheck 未通過）
- 或 flex_api user/password 錯誤

**解決**:
```bash
# 檢查 db_mysql 狀態
docker compose ps | grep db_mysql

# 查看 flex_api 日誌
docker compose logs flex_api --tail 50

# 手動驗證 DB 連線
mysql -h 127.0.0.1 -P 13366 -u flex_api -p line_flex -e "SELECT 1"
```

### 4.4 Dify workflow 無法連線到 flex_api

**症狀**: fetch_flex 報 "connection refused" 或 "Host not found"

**原因**: Dify 容器無法解析 `flex_api` hostname

**解決**:
```bash
# 確認 flex_api 在同一 docker network
docker inspect docker-flex_api-1 | grep Networks

# 若在不同 network，需在 docker-compose.yaml 加 networks 設定
# 或改用 host.docker.internal (macOS/Windows only)
```

---

## 5. 效能與安全

### 5.1 效能優化

- **快取**: 可在 flex_api 層加 Redis 快取 `flex_message_templates`
- **批量操作**: POST `/flex` 改支援陣列批量 upsert
- **分頁**: GET `/flex` 加 limit/offset 支援（目前全量返回）

### 5.2 安全考量

- **身份驗證**: 目前 flex_api 無認證，生產環境應加 API key 或 JWT
- **SQL 注入**: 已使用參數化查詢，安全
- **敏感資訊**: `FLEX_API_DB_PASSWORD` 改用強密碼，不要用預設值
- **CORS**: 若 Dify 與 flex_api 跨域，需設定 CORS 白名單

---

## 6. 未來擴展

### 6.1 短期 (v1.1)

- [ ] 後台管理介面（CRUD 模板，而非 API 直呼）
- [ ] 模板版本控制（保留歷史版本）
- [ ] 快取層（Redis）
- [ ] 模板預覽功能（web UI）

### 6.2 中期 (v2.0)

- [ ] 多語言支援（模板本地化）
- [ ] A/B 測試（多版本投放）
- [ ] 分析儀表板（模板點擊率、轉換率）
- [ ] 與 Dify dataset 整合（動態內容填充）

### 6.3 長期 (v3.0)

- [ ] 模板視覺化編輯器（Drag-and-drop）
- [ ] 與 CRM 整合（客戶分群投放）
- [ ] 實時更新通知（Webhook）
- [ ] 多平台支援（Facebook Messenger, WeChat 等）

---

## 7. 檔案清單

### 新建檔案

| 路徑 | 說明 |
|------|------|
| `flex-api/main.py` | FastAPI 應用程式入點 |
| `flex-api/requirements.txt` | Python 相依套件 |
| `flex-api/Dockerfile` | Docker image 定義 |
| `flex-api/.env.example` | 環境變數範例 |
| `flex-api/README.md` | API 文件 |
| `flex-api/sql/init.sql` | 資料庫初始化腳本 |
| `flex-api/sql/_generate_init.py` | 一次性: 從原 DSL 生成 init.sql |
| `flex-api/sql/_seed_from_line_flex_message.py` | 遷移 LineFlexMessage JSON 檔 |
| `flex-api/sql/_verify.py` | 驗證工具 |
| `DSL/Line_多選項連動助理_DB版.yml` | 新 workflow DSL（DB 驅動） |

### 修改檔案

| 路徑 | 修改內容 |
|------|---------|
| `dify/docker/docker-compose-template.yaml` | db_mysql 加 ports + volume; 新增 flex_api service |
| `dify/docker/docker-compose.yaml` | 自動生成（勿手編） |
| `dify/docker/docker-compose-gyro.yaml` | 同上（備用檔，通常用 template） |

### 保留檔案（參考用）

| 路徑 | 用途 |
|------|------|
| `DSL/Line_多選項連動助理_涵蓋所有FLEX_MESSAGE功能.yml` | 原版（含硬編碼） |
| `LineFlexMessage/*.json` | 模板來源檔 |

---

## 8. 總結

此次重構將 **硬編碼模板** 轉變為 **資料庫驅動架構**，實現了：

✅ **解耦**: 業務邏輯（workflow）與資料（模板）分離  
✅ **可維護性**: 模板無需改 DSL，直接修改 DB  
✅ **可擴展性**: 新增模板無需重新部署 workflow  
✅ **標準化**: FastAPI 提供 REST 介面，支援 CRUD 操作  
✅ **規範性**: 遵循專案既有慣例（FastAPI、Docker、MySQL）  

**下一步**: 考慮建立後台管理 UI，讓非技術人員也能維護模板。

---

## 9. LINE Channel 設定遷移（v1.1）

**日期**: 2026-04-22
**範圍**: 僅 `DSL/Line_多選項連動助理_DB版.yml`，不影響其他 DSL
**目標**: 將 `LINE_CHANNEL_ACCESS_TOKEN` 與 `LINE_USER_ID` 兩個值從 Dify 環境變數移到 MySQL，由 flex-api 提供 REST 讀取

### 9.1 背景問題

v1.0 完成後，Flex Message 模板已 DB 化，但 LINE 憑證仍硬編碼在 DSL 的 `environment_variables` 區段（`value_type: secret` 僅做 UI 遮罩，YAML 匯出時是明文）：

```yaml
environment_variables:
- name: LINE_CHANNEL_ACCESS_TOKEN
  value: xv7a1j7jR8o22tgsLvOY...    # 明文外洩風險
  value_type: secret
- name: LINE_USER_ID
  value: Uc83af6e58fd43c6da...
  value_type: string
```

衍生三個問題：

- 匯出 / 分享 DSL 時 token 會進 git 或傳檔
- 換 bot、換目標 user 要重新改 DSL 匯入匯出
- 與「DB 版」命名不符，Flex 走 DB 但憑證未走

### 9.2 設計決策

| 項目 | 選擇 | 未採用選項 |
|---|---|---|
| Table 結構 | **專用 `line_channels` table**（強型別欄位） | 泛型 `app_settings(name, value)` key-value |
| API 風格 | **`GET /line/channel/{name}` 一次回傳整組** | `GET /config/{name}` 單值、DSL 需呼兩次 |
| 多 channel 支援 | **暫只做 `default` 單一 channel** | DSL 增 `channel_name` 輸入，未來擴充 |

### 9.3 新資料表：`line_channels`

#### Schema

```sql
CREATE TABLE IF NOT EXISTS line_channels (
  name                  VARCHAR(64)  NOT NULL PRIMARY KEY,
  channel_access_token  TEXT         NOT NULL,
  default_user_id       VARCHAR(64)  NOT NULL,
  description           VARCHAR(255) NULL,
  created_at            TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
  updated_at            TIMESTAMP    DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

| 欄位 | 類型 | 說明 |
|---|---|---|
| `name` | VARCHAR(64) PK | channel 邏輯名稱（目前固定用 `default`，未來可多個 bot） |
| `channel_access_token` | TEXT NOT NULL | LINE Messaging API 的 long-lived access token |
| `default_user_id` | VARCHAR(64) NOT NULL | 預設 push 目標的 LINE userId |
| `description` | VARCHAR(255) NULL | 人類可讀說明（哪個 bot、誰用的） |
| `created_at` | TIMESTAMP | 建立時間 |
| `updated_at` | TIMESTAMP | 最後修改時間（自動維護） |

#### Seed 資料

```sql
INSERT INTO line_channels (name, channel_access_token, default_user_id, description) VALUES
('default',
 'xv7a1j7jR8o22tgsLvOY...（省略，完整見 init.sql）',
 'Uc83af6e58fd43c6da36a9285435a82e0',
 'main LINE bot (migrated from DSL env vars)')
ON DUPLICATE KEY UPDATE
  channel_access_token = VALUES(channel_access_token),
  default_user_id      = VALUES(default_user_id),
  description          = VALUES(description);
```

> **安全備註**：token 目前以明文存放於 DB，與 `flex_message_templates` 同層防護（僅 Docker 內網可達、`flex_api` user 無 DROP 權限）。若後續需加密，建議統一在 DB 層（如 MySQL `AES_ENCRYPT`）或 flex-api 服務層處理，而非只保護此單表。

### 9.4 `line_flex` 資料庫 Schema 總覽（合併 v1.0 + v1.1）

| Table | 功能 | 主鍵 | 建立版本 |
|---|---|---|---|
| `flex_message_templates` | Flex Message 模板內容 | `id` (VARCHAR 64) | v1.0 |
| `line_channels` | LINE bot 憑證與目標 user | `name` (VARCHAR 64) | v1.1 |

完整 DDL 集中於 [flex-api/sql/init.sql](flex-api/sql/init.sql)，由 [flex-api/sql/_generate_init.py](flex-api/sql/_generate_init.py) 產生（產生器模板已同步更新，重跑不會覆寫 `line_channels`）。

### 9.5 flex-api 新增 endpoint

| Method | Path | 用途 | Response |
|---|---|---|---|
| GET | `/line/channel/{name}` | 取得指定 channel 的憑證與預設 userId | `{name, channel_access_token, default_user_id, description}` |

實作 ([flex-api/main.py](flex-api/main.py)) 對齊既有 `GET /flex/{flex_id}` 風格：

```python
class LineChannelOut(BaseModel):
    name: str
    channel_access_token: str
    default_user_id: str
    description: Optional[str] = None


@app.get("/line/channel/{name}", response_model=LineChannelOut)
def get_line_channel(name: str):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT name, channel_access_token, default_user_id, description "
            "FROM line_channels WHERE name=%s",
            (name,),
        )
        row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail=f"line channel '{name}' not found")
    return row
```

> 暫未實作 POST/PUT/DELETE（YAGNI）。設定變更走 DB 直接 UPDATE，未來有管理需求再補 CRUD。

### 9.6 DSL workflow 變更

#### 變更前後流程對比

```
v1.0:  start → fetch_flex → assemble → send_line → answer
v1.1:  start → fetch_line_config → extract_line_config → fetch_flex → assemble → send_line → answer
```

新增兩個節點（位於 start 與 fetch_flex 之間）：

**(1) fetch_line_config (HTTP GET)**

```yaml
url: '{{#env.FLEX_API_BASE_URL#}}/line/channel/default'
method: get
authorization: no-auth
timeout: { connect: 3, read: 5, write: 5, max_execution_time: 10 }
```

**(2) extract_line_config (Code - Python3)**

```python
import json

def main(fetch_body: str, status_code: int) -> dict:
    if status_code != 200:
        return {"token": "", "user_id": "", "error": "true",
                "error_msg": f"failed to fetch line channel config (HTTP {status_code})"}
    try:
        parsed = json.loads(fetch_body)
    except Exception as e:
        return {"token": "", "user_id": "", "error": "true",
                "error_msg": f"invalid line channel config response: {e}"}
    return {
        "token": parsed.get("channel_access_token", ""),
        "user_id": parsed.get("default_user_id", ""),
        "error": "false",
        "error_msg": "",
    }
```

outputs: `token`, `user_id`, `error`, `error_msg`

**(3) send_line 引用改寫**

| 欄位 | v1.0 | v1.1 |
|---|---|---|
| headers | `Authorization:Bearer {{#env.LINE_CHANNEL_ACCESS_TOKEN#}}` | `Authorization:Bearer {{#extract_line_config.token#}}` |
| body `to` | `{{#env.LINE_USER_ID#}}` | `{{#extract_line_config.user_id#}}` |

**(4) answer 節點錯誤處理**

從單層條件擴充成兩層（優先檢查上游 channel 設定錯誤）：

```
{{#extract_line_config.error#=="true"
   ? extract_line_config.error_msg
   : (#assemble.error#=="true" ? assemble.error_msg
       : ("OK! 已發送 flex_id=" + #start.flex_id# + " 至 LINE (status=" + #send_line.status_code# + ")"))}}
```

#### environment_variables

DSL 中的 `LINE_CHANNEL_ACCESS_TOKEN` 與 `LINE_USER_ID` 兩個 env var 定義**已刪除**，僅保留 `FLEX_API_BASE_URL`（仍需用來指向 flex-api）。

### 9.7 部署步驟

> `init.sql` 只在 MySQL 首次啟動且 datadir 空時執行。Schema 變更後需以下兩步同步部署，兩步都冪等、可重跑：

```bash
# 1. 套用新 schema 到既有 DB（CREATE TABLE IF NOT EXISTS + ON DUPLICATE KEY UPDATE）
docker exec -i docker-db_mysql-1 mysql -uroot -p"$DB_PASSWORD" < flex-api/sql/init.sql

# 2. 驗證 seed 寫入
docker exec -it docker-db_mysql-1 mysql -uflex_api -pflex_api_pwd_change_me line_flex \
  -e "SELECT name, default_user_id, LEFT(channel_access_token, 20) AS token_prefix FROM line_channels;"

# 3. 重建 flex_api image 以載入新 endpoint
cd dify/docker
docker compose -f docker-compose-gyro.yaml --profile mysql up -d --build flex_api

# 4. 驗證 endpoint
curl -s http://localhost:8002/line/channel/default | python -m json.tool

# 5. 在 Dify 後台重新匯入 DSL/Line_多選項連動助理_DB版.yml（舊 app 建議先刪，避免 env var 殘留）
```

> container 名稱依 compose project name 決定。本專案實際啟動目錄為 `dify/docker/`，因此 container 名為 `docker-db_mysql-1`、`docker-flex_api-1`（不是早期文件提到的 `dify-*` 前綴）。

### 9.8 驗證結果

| 測試 | 實際結果 |
|---|---|
| `GET /line/channel/default` | 200，回傳完整 `{name, channel_access_token, default_user_id, description}` |
| `GET /line/channel/nonexistent` | 404 `{"detail":"line channel 'nonexistent' not found"}` |
| DSL workflow 端對端 | fetch_line_config 200 → extract_line_config 正常 parse → fetch_flex 200 → send_line 200，LINE 收到訊息 |
| 其他非 DB 版 DSL | 不受影響（本次改動只碰 `Line_多選項連動助理_DB版.yml`） |

### 9.9 檔案異動清單（v1.1）

| 路徑 | 類型 | 改動 |
|---|---|---|
| `flex-api/sql/init.sql` | 修改 | 新增 `line_channels` CREATE 與 `default` seed |
| `flex-api/sql/_generate_init.py` | 修改 | 產生器模板同步，重跑不會覆寫 `line_channels` |
| `flex-api/main.py` | 修改 | 新增 `LineChannelOut` model + `GET /line/channel/{name}` handler |
| `DSL/Line_多選項連動助理_DB版.yml` | 修改 | 移除 2 個 env vars、插入 2 個節點、改 2 條→6 條 edges、重寫 send_line 引用、answer 合併錯誤處理 |

### 9.10 未做的事（留待後續）

- ❌ 舊 DSL 檔案中仍含明文 token，若已進 git 歷史需另行用 `git filter-repo` 清除
- ❌ 其他 LINE DSL（不含「DB版」命名）仍用 Dify env vars，未遷移
- ❌ 未加密 `channel_access_token`；若升級加密需統一在 DB 或 service 層處理
- ❌ 未實作 POST/PUT/DELETE `/line/channel`；設定變更暫走 SQL UPDATE
- ❌ 未支援多 channel；DSL 寫死 `name=default`，擴充時需在 start 節點加輸入欄

---

**整理人：Claude Code & Porter**

