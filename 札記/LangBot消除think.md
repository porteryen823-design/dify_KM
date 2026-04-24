# LangBot 消除 Dify 回應中的 `<think>` 標籤指南

> **建立日期：** 2026-04-10
> **整理人：** Antigravity AI & Porter

---

## 一、問題背景

當使用 DeepSeek 或 R1 等具備思維鏈（Chain of Thought）能力且輸出格式包含 `<think>` 標籤的模型時，LangBot 接收到的原始回應會包含冗長的思考過程。這在一般對話（如 Telegram/Discord）中會影響閱讀體驗。

---

## 二、⚠️ 重要：配置儲存位置（容易踩坑！）

`remove-think` 設定**並非**存在 `pipeline_config.json`，而是儲存於 **SQLite 資料庫**。

| 位置 | 說明 |
|------|------|
| ~~`/app/data/pipeline_config.json`~~ | 僅為新建 Pipeline 的**預設模板**，修改後對已存在的 Pipeline **無效** |
| `/app/data/langbot.db` | **實際生效的配置**，儲存於 `legacy_pipelines` 資料表的 `config` 欄位（JSON 格式）|

若只修改 `pipeline_config.json` 後重啟，已存在的 Pipeline 設定不會改變，`<think>` 標籤仍會出現。

---

## 三、正確修復方式（直接更新 SQLite DB）

### Step 1：將資料庫複製到宿主機

```powershell
docker cp dify-langbot:/app/data/langbot.db C:\VSCode_Proj\Dify\backups\langbot_inspect.db
```

### Step 2：在宿主機執行修復腳本（更新全部 Pipeline）

```python
# fix_remove_think.py  （已存放於 C:\VSCode_Proj\Dify\backups\）
import sqlite3
import json

DB_PATH = r"C:\VSCode_Proj\Dify\backups\langbot_inspect.db"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row

rows = conn.execute("SELECT uuid, name, config FROM legacy_pipelines").fetchall()
updated = []

for row in rows:
    uuid = row['uuid']
    name = row['name']
    config_raw = row['config']
    if not config_raw:
        continue
    try:
        cfg = json.loads(config_raw)
        cfg['output']['misc']['remove-think'] = True  # ← 核心設定
        new_config = json.dumps(cfg, ensure_ascii=False)
        conn.execute(
            "UPDATE legacy_pipelines SET config = ? WHERE uuid = ?",
            (new_config, uuid)
        )
        updated.append(f"  [{uuid[:8]}...] {name}")
    except Exception as e:
        print(f"Error: {name}: {e}")

conn.commit()
conn.close()

print("=== 已更新 Pipelines ===")
for u in updated:
    print(u)
```

### Step 3：將資料庫回寫進容器

```powershell
docker cp C:\VSCode_Proj\Dify\backups\langbot_inspect.db dify-langbot:/app/data/langbot.db
```

### Step 4：重啟容器使配置生效

```powershell
docker restart dify-langbot
```

---

## 四、驗證修復結果

重啟後，可執行以下指令確認所有 Pipeline 是否已設定成功：

```powershell
# Step 1: 取出最新 DB
docker cp dify-langbot:/app/data/langbot.db C:\VSCode_Proj\Dify\backups\langbot_verify.db

# Step 2: 列出每條 Pipeline 的 remove-think 值（期望全部為 True）
python -c "
import sqlite3, json
conn = sqlite3.connect(r'C:\VSCode_Proj\Dify\backups\langbot_verify.db')
rows = conn.execute('SELECT name, config FROM legacy_pipelines').fetchall()
for name, cfg in rows:
    val = json.loads(cfg)['output']['misc'].get('remove-think')
    print(f'{name}: remove-think = {val}')
"
```

---

## 五、替代方案：在 Dify Workflow 端過濾

若不希望在 LangBot 端處理，可在 Dify 工作流中加入 **Code 節點**：

```python
import re

def main(text: str):
    # 使用正則移除 <think>...</think> 區塊（支援跨行）
    cleaned_text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()
    return {
        "result": cleaned_text
    }
```

**插入位置：** LLM 節點 ➔ **Code 節點 (清洗)** ➔ 直接輸出 (Answer)

---

## 六、技術細節：Plugin 過濾邏輯

插件 `difysvapi_langbot_plugin.py` 的過濾機制：

- **讀取設定：** `self.pipeline_config['output']['misc'].get('remove-think')`
- **正規模式：** `r'<think>(.*?)</think>'`（配合 `re.DOTALL` 跨行匹配）
- **處理函數：** `_process_thinking_content()`
- **行為：**
    - `remove-think = true`：完全刪除 `<think>` 標籤及其所有內容
    - `remove-think = false`：保留思考內容，放在回應最前端

---

## 七、維護建議

1. **配置持久化**：建議將 `/app/data/langbot.db` 透過 Docker Volume 掛載到宿主機，避免容器升級後資料庫被覆蓋，修改全部失效。
2. **新增 Pipeline 後記得處理**：新建的 Pipeline 初始 `remove-think` 仍為 `false`，建議新增後重新執行 `fix_remove_think.py` 腳本。
3. **多管齊下**：建議同時在 Dify Workflow 端也進行 Code 節點清洗，雙重保障確保輸出乾淨。
