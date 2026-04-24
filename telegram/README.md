# Dify Telegram 整合指南 (Health Check Alert)

本文件紀錄了 Dify 系統與 Telegram Bot 的整合設定，主要用於 Ollama 或其他外部 API 發生異常時，能夠即時推送格式化告警訊息到 Telegram 頻道/私訊中。

---

## 1. 核心驗證資訊 (Credentials)

| 項目 | 數值 | 說明 |
| :--- | :--- | :--- |
| **機器人名稱 (Bot)** | `@porter_telegram_bot` | 用於推送告警的 Telegram 機器人 |
| **API Token** | `請放在 telegram/.env` | 從 BotFather 申請的通訊金鑰 |
| **目標 Chat ID** | `請放在 telegram/.env` | 接收私訊的 User ID |

---

## 2. API 呼叫設定 (Dify HTTP 節點)

若要在 Dify 或 n8n 中手動建立 Telegram 告警節點，請參照以下設定：

*   **HTTP Method**: `POST`
*   **API URL (含 Token)**: 
    ```text
    https://api.telegram.org/bot<TOKEN>/sendMessage
    ```
*   **Headers**:
    ```json
    {
      "Content-Type": "application/json"
    }
    ```

---

## 3. JSON 負載模板 (Payload)

⚠️ **排版注意事項 (parse_mode)**: 
強烈建議使用 `HTML` 模式代替 `MarkdownV2`。因為 Telegram 的 MarkdownV2 對特殊字元（如 `-`, `.`, `{`）的跳脫 (escape) 非常嚴格，在 Dify 變數替換時非常容易引發 `400 Bad Request` 錯誤。

**HTML 格式範例：**
```json
{
  "chat_id": "<CHAT_ID>",
  "text": "⚠️ <b>Ollama 狀態告警</b>\n\n檢查到遠端 Ollama API 無法正常連線，可能導致知識庫無法使用。\n\n⏳ <b>狀態碼</b>: <code>{{#http_test.status_code#}}</code>\n📌 <b>API 位址</b>: <code>http://gyro1.ddns.net:11434</code>\n🔍 <b>偵測時間</b>: <code>{{#time_formatter.formatted_time#}}</code>",
  "parse_mode": "HTML"
}
```

---

## 4. 時間處理腳本 (Python 節點)

與 Discord 可以吃 UNIX 時間戳並自動呈現相對時間（如 `<t:unix:R>`）不同，Telegram 不支援動態時間標籤。因此，必須在呼叫 HTTP 請求前，在 Dify 中建立一個 `Python code` 節點，將系統毫秒轉換成當地時區（台北 UTC+8）的易讀字串：

**輸入變數**: `timestamp_ms` (對應 `sys.query_timestamp`)

```python
import time
from datetime import datetime, timezone, timedelta

def main(timestamp_ms):
    try:
        # 若系統提供有效時間戳則取用，否則抓取當下時間
        ms = int(timestamp_ms) if timestamp_ms is not None else int(time.time() * 1000)
    except:
        ms = int(time.time() * 1000)
    
    # 轉換為台北時間 (UTC+8)
    dt = datetime.fromtimestamp(ms / 1000, tz=timezone(timedelta(hours=8)))
    time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    
    return {
        "formatted_time": time_str
    }
```
*在後續的 HTTP 節點中即可使用 `{{#time_formatter.formatted_time#}}` 來調用時間。*

---

## 5. API 測試指引 (PowerShell 範例)

若要在本機（例如 Windows PowerShell）環境中快速驗證 Token 是否生效、或是想測試推播功能的連通性，可以直接執行以下命令：

```powershell
Invoke-RestMethod -Uri "https://api.telegram.org/bot8552004716:AAGo0eNqPwk6towDeK0z8X8amMVEujdqRN4/sendMessage" -Method Post -ContentType "application/json" -Body '{"chat_id": "8226231440", "text": "✅ *測試成功* \n\nAntigravity AI 已成功連線至您的 Telegram，這也代表 Dify 告警功能設定就緒啦！", "parse_mode": "Markdown"}'
Invoke-RestMethod -Uri "https://api.telegram.org/bot<TOKEN>/sendMessage" -Method Post -ContentType "application/json" -Body '{"chat_id": "<CHAT_ID>", "text": "Test message", "parse_mode": "HTML"}'
```

---

## 6. 故障排除與技巧 (Troubleshooting)

### Q: 如何取得其他人的Chat ID 或 群組 Chat ID？
**私訊 ID：**
請對方在 Telegram 搜尋並私訊 `@userinfobot`，該機器人會回傳的 `Id:` 就是個人的 Chat ID。

**群組 ID：**
1. 將本告警機器人 (`@porter_telegram_bot`) 拉入群組。
2. 將 `@getmyid_bot` 加進去，它會主動回應 `"Current chat ID: -100xxxxxxxxx"`（群組通常含有負號）。
3. 也可以透過指令拉取：`Invoke-RestMethod -Uri "https://api.telegram.org/bot<TOKEN>/getUpdates" -Method Get` 在 `chat` 物件中尋找。

### Q: 遇到 400 Bad Request : chat not found
代表 JSON 中的 `"chat_id"` 欄位填入了無效的數值（例如文字 placeholder 或是錯誤的 ID）。

### Q: 遇到 409 Conflict: webhook is active
這是因為該 Token 先前可能被 n8n 或其他服務註冊了 Webhook，此時若是想用 `getUpdates` 偷偷拉取聊天紀錄會被拒絕。但不影響主動發送告警 (`sendMessage`) 的功能。若要解除，可調用 `/deleteWebhook` 端點。

---

**整理人：** Antigravity AI & Porter  
**更新日期：** 2026-03-31
