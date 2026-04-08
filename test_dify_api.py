import sys
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

# Dify Workflow API Endpoint
url = 'http://localhost:8080/v1/workflows/run'

# API Key 從你的截圖中取得
API_KEY = 'app-wN0JfZROuXA5DClC4T8kpaLI'

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# 傳送給 Workflow 的資料
payload = {
    "inputs": {
        "query": "嗨！這是一則來自 test.py 的測試訊息，請問你有收到嗎？請簡短回答。"
    },
    "response_mode": "blocking", # 等待整段結果產生完才一次回傳
    "user": "test-user-123"
}

print("正在發送 API 請求到 Dify...")
try:
    response = requests.post(url, headers=headers, json=payload)
    
    print(f"\n狀態碼 (Status Code): {response.status_code}")
    
    if response.status_code == 200:
        print("\n[成功] 請求成功！以下是回傳結果：")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
        # 嘗試解析我們設定的 summary 欄位
        response_data = response.json()
        if "data" in response_data and "outputs" in response_data["data"]:
            if "summary" in response_data["data"]["outputs"]:
                print("\n================== 擷取到的 LLM 回覆 ==================")
                print(response_data["data"]["outputs"]["summary"])
                print("======================================================")
            else:
                 print("\n[警告]：回傳的資料中沒有找到 'summary' 變數。請檢查 AAA.yml 的輸出節點。")
    else:
        print("\n[失敗] 請求失敗！")
        print(response.text)

except Exception as e:
    print(f"\n[錯誤] 發生錯誤: {e}")
