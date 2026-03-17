# 設定 Discord 與 Dify 串接指南

本指南用於說明如何將 Dify 的 Advanced Chat 應用與 Discord 串接。以「桃花源問答」為例。

## 整體架構

```
Discord 用戶
    ↓ 發送訊息
Discord Bot (自建)
    ↓ 呼叫 Dify API (HTTP POST)
Dify 桃花源問答應用
    ↓ RAG + 回答
Discord Bot 將回答貼回頻道
```

## 步驟一：取得 Dify API Key

1. 進入 Dify 後台選擇您的應用（如：桃花源 問答）。
2. 左側選單點選「**API 存取**」（或「發布 → API」）。
3. 記下以下資訊：
   - **API Base URL**：例如 `http://your-dify-host/v1`
   - **API Key**：形如 `app-xxxxxxxxxxxxxxxx`

## 步驟二：建立 Discord Bot

1. 前往 [Discord Developer Portal](https://discord.com/developers/applications)。
2. 建立新 Application → Bot → 複製 **Bot Token**。
3. 在 Bot 頁面開啟以下 **Privileged Gateway Intents**：
   - `MESSAGE CONTENT INTENT`
4. 透過 OAuth2 → URL Generator 邀請 Bot 入群（需要 `bot` 權限，以及 `Send Messages`, `Read Message History`）。

## 步驟三：撰寫 Python Bridge 腳本

```python
# discord_dify_bridge.py
import discord
import requests
import os
import sys
import io

# Windows UTF-8 修正
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DISCORD_BOT_TOKEN = "YOUR_DISCORD_BOT_TOKEN"
DIFY_API_KEY      = "app-xxxxxxxxxxxxxxxx"
DIFY_BASE_URL     = "http://your-dify-host/v1"

# 儲存每個 Discord 用戶的 conversation_id（多輪對話用）
conversation_map: dict[str, str] = {}

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def query_dify(user_id: str, question: str) -> str:
    """呼叫 Dify Chat API，維護多輪對話"""
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "inputs": {},
        "query": question,
        "response_mode": "blocking",   # 阻塞模式，等待完整回答
        "user": user_id,
    }
    # 若該用戶已有對話紀錄，延續同一個 conversation
    if user_id in conversation_map:
        payload["conversation_id"] = conversation_map[user_id]

    resp = requests.post(f"{DIFY_BASE_URL}/chat-messages", headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    # 保存 conversation_id 以供後續多輪對話
    conversation_map[user_id] = data.get("conversation_id", "")

    return data.get("answer", "（無法取得回答）")

@client.event
async def on_ready():
    print(f"Bot 已上線：{client.user}")

@client.event
async def on_message(message: discord.Message):
    # 忽略 Bot 自己的訊息
    if message.author.bot:
        return

    # 指定頻道才回應（可選，防止 Bot 到處亂答）
    # if message.channel.id != YOUR_CHANNEL_ID:
    #     return

    user_id = str(message.author.id)
    question = message.content.strip()
    if not question:
        return

    async with message.channel.typing():
        try:
            answer = query_dify(user_id, question)
        except Exception as e:
            answer = f"⚠️ 呼叫 Dify 發生錯誤：{e}"

    # Discord 單則訊息上限 2000 字元
    if len(answer) > 2000:
        answer = answer[:1997] + "..."

    await message.reply(answer)

client.run(DISCORD_BOT_TOKEN)
```

## 步驟四：安裝依賴並執行

```powershell
# 建立虛擬環境
python -m venv venv
.\venv\Scripts\activate

# 安裝套件
pip install discord.py requests

# 執行 Bot
python discord_dify_bridge.py
```

## 關鍵 API 說明
| 項目 | 值 |
|------|-----|
| API 模式 | `advanced-chat` → 使用 `/v1/chat-messages` |
| 回應模式 | `blocking`（簡易）或 `streaming`（串流） |
| 多輪對話 | 透過 `conversation_id` 維持，Bot 幫每位用戶保存 |
| `user` 參數 | 傳入 Discord User ID 作為識別 |

**注意**：若 Dify 使用本地模型（如 Ollama），Dify 服務需在本地或透過內網運行，Discord Bot 才能存取。若對外服務，則 Dify 需有外部可訪問的 URL（如 Ngrok 或固定 IP）。
**整理人：** Antigravity AI & Porter
