# Discord 告警與 Bot 整合資訊

本文件整理了用於 Dify 系統監控與外部服務告警的 Discord Bot 資訊。

## 1. Bot 與 頻道資訊 (生產環境)

*   **專案參考**: `OpenClaw`
*   **Discord Bot Token**: `YOUR_DISCORD_TOKEN` (已匯入 Dify 系統)
*   **告警目標頻道 (Channel ID)**: `1439192827077857393`

---

## 2. API 使用規範 (Dify HTTP Node)

在 Dify 工作流中發送 Discord 訊息時，請遵循以下設定：

### HTTP 設定
*   **Method**: `POST`
*   **URL**: `https://discord.com/api/v10/channels/{CHANNEL_ID}/messages`
*   **Headers**: 
    - `Content-Type: application/json`
    - `Authorization: Bot {BOT_TOKEN}`

---

## 3. 告警 UI 美編範本 (Embeds)

用於 `ollama_healthcheck` 機器人的標準美編 JSON 格式：

```json
{
  "embeds": [
    {
      "title": "⚠️ Ollama 狀態告警",
      "description": "檢查到遠端 Ollama API 無法正常連線，可能導致知識庫無法使用。",
      "color": 16711680,
      "fields": [
        {
          "name": "⏳ 狀態碼",
          "value": "`{{#http_test.status_code#}}`",
          "inline": true
        },
        {
          "name": "📌 API 位址",
          "value": "`http://gyro1.ddns.net:11434`",
          "inline": true
        },
        {
          "name": "🔍 偵測時間",
          "value": "<t:{{#timestamp_fix.unix_sec#}}:R>",
          "inline": false
        }
      ],
      "footer": {
        "text": "Dify Health Checker @ AWS Gyro"
      }
    }
  ]
}
```

---

## 4. 時間戳記處理 (重要)

*   **問題**: Dify 系統變數 `sys.query_timestamp` 為**毫秒 (ms)**，但 Discord 標記語法 `<t:timestamp:R>` 需要**秒 (sec)**。
*   **解決方案**: 在 HTTP 節點前加入 `Python3` 節點進行轉換：
    ```python
    import time
    def main(timestamp_ms):
        try:
            ms = int(timestamp_ms) if timestamp_ms is not None else int(time.time() * 1000)
        except:
            ms = int(time.time() * 1000)
        return { "unix_sec": int(ms / 1000) }
    ```

---

## 5. Telegram 告警整合資訊

若要改用 Telegram 進行告警，請參考以下設定：

*   **Telegram Bot Token**: `8552004716:AAGo0eNqPwk6towDeK0z8X8amMVEujdqRN4`
*   **Bot Username**: `@porter_telegram_bot`
*   **API URL**: `https://api.telegram.org/bot8552004716:AAGo0eNqPwk6towDeK0z8X8amMVEujdqRN4/sendMessage`

### HTTP 設定 (Telegram)
*   **Method**: `POST`
*   **Headers**: 
    - `Content-Type: application/json`

### JSON Body (強制使用 HTML Parse Mode)
⚠️ **注意**: 為了避免 Markdown 特殊符號驗證崩潰，Telegram 建議使用 `HTML` 格式：

```json
{
  "chat_id": "REPLACE_WITH_YOUR_CHAT_ID",
  "text": "⚠️ <b>Ollama 狀態告警</b>\n\n檢查到遠端 Ollama API 無法正常連線，可能導致知識庫無法使用。\n\n⏳ <b>狀態碼</b>: <code>{{#http_test.status_code#}}</code>\n📌 <b>API 位址</b>: <code>http://gyro1.ddns.net:11434</code>\n🔍 <b>偵測時間</b>: <code>{{#time_formatter.formatted_time#}}</code>",
  "parse_mode": "HTML"
}
```

### 時間處理差異 (Telegram)
Telegram 不支援 Discord 的 `<t:unix:R>` 相對時間排版，因此 Python 節點需要改為直接輸出**格式化字串 (如台北時間 YYYY-MM-DD HH:MM:SS)**：

```python
import time
from datetime import datetime, timezone, timedelta

def main(timestamp_ms):
    try:
        ms = int(timestamp_ms) if timestamp_ms is not None else int(time.time() * 1000)
    except:
        ms = int(time.time() * 1000)
    
    dt = datetime.fromtimestamp(ms / 1000, tz=timezone(timedelta(hours=8)))
    return { "formatted_time": dt.strftime("%Y-%m-%d %H:%M:%S") }
```

---

**整理人：** Antigravity AI & Porter  
**更新日期：** 2026-03-31
