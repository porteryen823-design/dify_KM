import sys
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

# Dify Workflow API Endpoint
url = 'http://localhost:8080/v1/workflows/run'

# API Key
API_KEY = 'app-wN0JfZROuXA5DClC4T8kpaLI'

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# 傳送給 Workflow 的資料 (Streaming mode)
payload = {
    "inputs": {
        "query": "嗨！這是一則來自 test_streaming.py 的測試訊息，請問你有收到嗎？請簡短回答。"
    },
    "response_mode": "streaming",
    "user": "test-user-streaming"
}

print("正在發送 Streaming API 請求到 Dify...")
try:
    response = requests.post(url, headers=headers, json=payload, stream=True)
    
    print(f"\n狀態碼 (Status Code): {response.status_code}")
    
    if response.status_code == 200:
        print("\n[成功] 請求成功！開始接收串流數據：")
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                print(f"收到數據: {decoded_line}")
                if decoded_line.startswith('data:'):
                    try:
                        data = json.loads(decoded_line[5:])
                        if data.get('event') == 'workflow_finished':
                             print("\n[完成] 工作流執行結束。")
                    except:
                        pass
    else:
        print("\n[失敗] 請求失敗！")
        print(response.text)

except Exception as e:
    print(f"\n[錯誤] 發生錯誤: {e}")
