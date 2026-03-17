import requests
import json
import sys
import io

# 遵循 Antigravity Rules 8-1: Windows 環境特定規範，處理 Unicode 輸出編碼
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def main():
    # 設定目標伺服器位址與模型名稱@
    OLLAMA_URL = "http://192.168.0.126:11434/api/generate"
    MODEL_NAME = "gpt-oss:20b"
    #MODEL_NAME = "minimax-m2.5:cloud"
    # 準備發送給 Ollama 的內容
    payload = {
        "model": MODEL_NAME,
        "prompt": "你好，介紹一下你自己。",
        "stream": False  # 設定為 False 表示一次性獲取完整結果，不使用串流輸出
    }

    print(f"--- 正在連線至遠端 Ollama ({OLLAMA_URL}) ---")
    print(f"使用模型: {MODEL_NAME}")

    try:
        # 發送 POST 請求
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        
        # 檢查請求是否成功
        if response.status_code == 200:
            result = response.json()
            # 取得模型回應的文字內容
            ai_response = result.get("response", "")
            
            print("\n" + "="*50)
            print("【AI 回應內容】")
            print("-" * 50)
            print(ai_response)
            print("="*50)
            
            # 列印一些額外的統計資訊（選用）
            total_duration = result.get("total_duration", 0) / 1e9 # 轉換為秒
            print(f"\n回應耗時: {total_duration:.2f} 秒")
            
        else:
            print(f"\n[錯誤] 伺服器回傳狀態碼: {response.status_code}")
            print(f"錯誤訊息: {response.text}")

    except requests.exceptions.ConnectTimeout:
        print("\n[錯誤] 連線逾時！請檢查 192.168.0.126 的網路是否通暢，或防火牆是否開放 11434 埠位。")
    except requests.exceptions.ConnectionError:
        print("\n[錯誤] 無法建立連線。請確認目標電腦的 Ollama 是否正在運行，並已設定 OLLAMA_HOST=0.0.0.0。")
    except Exception as e:
        print(f"\n[發生非預期錯誤] {str(e)}")

if __name__ == "__main__":
    main()
