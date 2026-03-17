# Dify 機器人接入 Discord 規劃

## 總覽
本目錄 (`discord/`) 用於存放將 Dify 聊天機器人接入 Discord 頻道的相關代碼與技術文件。
核心架構為：Discord 使用者發言 -> Discord Bot (Python) 接收 -> 呼叫 Dify Chat API -> Dify 處理並回傳 -> Discord Bot 將結果回覆給使用者。

## 準備工作
1. **Discord 端：**
   - 前往 [Discord Developer Portal](https://discord.com/developers/applications) 建立一個新的 Application。
   - 啟用 Bot 功能，並取得 `Bot Token`。
   - 在 OAuth2 中產生邀請連結（啟用 `bot` scope 與 `Send Messages` 等權限），將機器人加入目標伺服器 (Server)。
   - 開啟 `Message Content Intent`（進入 Bot 分頁，將 MESSAGE CONTENT INTENT 打開，以便讀取使用者的訊息內容）。

2. **Dify 端：**
   - 進入 Dify 平台，打開已佈署的 Chatbot 應用。
   - 導航到「存取 API (API Access)」。
   - 生成並複製一組 `API Key`。
   - 取得 API 的 Base URL（若為官方版通常是 `https://api.dify.ai/v1`，如果是本地部署則是本地伺服器網址，如 `http://localhost/v1`）。

3. **環境變數 (.env)：**
   複製本目錄下的 `.env.example` 並重新命名為 `.env`，填入您的敏感資訊：
   ```env
   DISCORD_BOT_TOKEN=your_discord_bot_token_here
   DIFY_API_KEY=your_dify_api_key_here
   DIFY_API_BASE_URL=http://localhost/v1
   ```

## 執行方式
我們使用 Python 撰寫這個中介層 (Middleware) 機器人。

1. **安裝依賴套件：**
   建議建立虛擬環境後安裝套件。
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows 則使用 venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **啟動機器人：**
   ```bash
   python dify_discord_bot.py
   ```

3. **測試：**
   在 Discord 頻道中輸入訊息，機器人應該會將訊息轉發給 Dify，並將 Dify 的回答傳回頻道中。

**整理人：** Antigravity AI & Porter
