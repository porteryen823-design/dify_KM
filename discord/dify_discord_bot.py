import discord
import os
import requests
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DIFY_API_KEY = os.getenv('DIFY_API_KEY')
DIFY_API_BASE_URL = os.getenv('DIFY_API_BASE_URL', 'https://api.dify.ai/v1')

# 設定 Discord Intents
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def ask_dify(query: str, user_id: str) -> str:
    """呼叫 Dify Chat API"""
    url = f"{DIFY_API_BASE_URL}/chat-messages"
    headers = {
        'Authorization': f'Bearer {DIFY_API_KEY}',
        'Content-Type': 'application/json',
    }
    data = {
        "inputs": {},
        "query": query,
        "response_mode": "blocking",
        "conversation_id": "",
        "user": str(user_id)
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result.get('answer', 'Dify 沒有回傳答案。')
    except Exception as e:
        print(f"Error calling Dify API: {e}")
        return "抱歉，與 Dify 伺服器通訊時發生錯誤。"

@client.event
async def on_ready():
    print(f'已登入為 {client.user}')

@client.event
async def on_message(message):
    # 避免機器人自己回覆自己
    if message.author == client.user:
        return

    # 若需要特定前綴（例如 !ask）才觸發，可在此判斷並擷取文字
    # if not message.content.startswith('!ask'): return
    # query = message.content[len('!ask'):].strip()
    
    query = message.content

    # 顯示正在輸入中...
    async with message.channel.typing():
        answer = ask_dify(query, message.author.id)
        
    # 若訊息過長 (Discord 限制 2000 字元)，需要分段發送
    if len(answer) > 2000:
        for i in range(0, len(answer), 2000):
            await message.channel.send(answer[i:i+2000])
    else:
        await message.channel.send(answer)

if __name__ == '__main__':
    if not DISCORD_BOT_TOKEN or not DIFY_API_KEY:
        print("請確認已設定 DISCORD_BOT_TOKEN 與 DIFY_API_KEY 環境變數 (見 .env 檔)。")
    else:
        client.run(DISCORD_BOT_TOKEN)
