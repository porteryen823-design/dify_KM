import sys
import requests
import json
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover
    load_dotenv = None

# 設定 Windows 控制台輸出編碼為 UTF-8，防止中文亂碼
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

if load_dotenv is not None:
    env_path = Path(__file__).resolve().with_name(".env")
    load_dotenv(dotenv_path=env_path, override=False)


def _get_required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"找不到 {name}，請在 dify_api/.env 設定，例如：{name}=...")
    return value


def test_dify_chat():
    """
    測試 Dify Chat App API
    """
    api_key = _get_required_env("API_KEY")
    base_url = _get_required_env("BASE_URL").rstrip("/")
    endpoint = f"{base_url}/chat-messages"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": {
            "output_language": "繁體中文"
        },
        "query": "漁人是哪個朝代的人",
        "response_mode": "blocking", # 使用阻塞模式等待完整回傳
        "conversation_id": "",       # 第一次對話留空
        "user": "porter-tester"      # 使用者識別名稱
    }

    print(f"正在發送請求到: {endpoint}")
    print(f"測試題目: {payload['query']}")
    print("-" * 30)

    try:
        # 發送 POST 請求
        response = requests.post(endpoint, headers=headers, json=payload, timeout=60)
        
        # 檢查 HTTP 狀態碼
        response.raise_for_status()
        
        # 解析 JSON 結果
        result = response.json()
        
        answer = result.get('answer', '無回應內容')
        conv_id = result.get('conversation_id', 'N/A')
        
        print("\n[API 回應成功]")
        print(f"回答內容:\n{answer}")
        print("-" * 30)
        print(f"對話 ID (Conversation ID): {conv_id}")
        
    except requests.exceptions.HTTPError as e:
        print(f"\n[HTTP 錯誤]: {e}")
        if e.response is not None:
            print(f"伺服器訊息: {e.response.text}")
    except requests.exceptions.RequestException as e:
        print(f"\n[請求異常]: {e}")

if __name__ == "__main__":
    test_dify_chat()
