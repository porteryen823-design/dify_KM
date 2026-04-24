import os
import requests
from dotenv import load_dotenv

# 載入同一目錄下的 .env 檔案中的環境變數
load_dotenv()

# 取得 Discord Bot Token
bot_token = os.getenv("DISCORD_BOT_TOKEN")
channel_id = os.getenv("DISCORD_CHANNEL_ID")

if not bot_token:
    print("找不到 DISCORD_BOT_TOKEN，請檢查 .env 檔案的設定。")
    exit(1)

if not channel_id:
    print("找不到 DISCORD_CHANNEL_ID，請檢查 .env 檔案的設定。")
    exit(1)

# Discord v10 API 發送訊息的 URL
url = f"https://discord.com/api/v10/channels/{channel_id}/messages"

# 請求標頭 (Headers)
headers = {
    "Authorization": f"Bot {bot_token}",
    "Content-Type": "application/json"
}

# 訊息內容
payload = {
    "content": "哈囉！這是一條透過 Python `requests` 模組發出的測試訊息 🤖"
}

print(f"正在嘗試發送訊息到頻道 {channel_id} ...")

# 透過 requests 發送 HTTP POST 請求
try:
    session = requests.Session()
    session.trust_env = False
    response = session.post(url, headers=headers, json=payload)

    # 檢查狀態碼
    if response.status_code == 200:
        print("訊息發送成功！")
        # 可以印出成功回應的 JSON 資料
        # print("詳細回應:", response.json())
    else:
        print(f"發送失敗，狀態碼: {response.status_code}")
        print("詳細錯誤資訊:", response.text)

except Exception as e:
    print(f"Request failed: {e}")
