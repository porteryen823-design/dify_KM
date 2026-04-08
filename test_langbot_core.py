import httpx
import json
import asyncio
import re

async def test_langbot_logic():
    API_KEY = "app-wN0JfZROuXA5DClC4T8kpaLI"
    # 使用我們在容器內設定的 Nginx 對外映射 (8080)
    BASE_URL = "http://localhost:8080/v1" 
    
    def strip_xml_tags(text: str) -> str:
        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        text = re.sub(r'<context>|</context>', '', text)
        return text.strip()

    print(f"正在模擬 LangBot 邏輯連線到: {BASE_URL}/workflows/run")
    
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=300.0) as client:
        try:
            async with client.stream(
                'POST',
                'workflows/run', # 注意這裡沒斜線，因為我們修過代碼
                headers={'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'},
                json={
                    'inputs': {'query': '你好，這是一則模擬 LangBot 的精密測試。請簡短回答。'},
                    'user': 'test-user',
                    'response_mode': 'streaming'
                }
            ) as r:
                print(f"DEBUG: Status Code: {r.status_code}")
                if r.status_code != 200:
                    print(f"錯誤: {r.status_code}")
                    return

                final_answer = ""
                async for line in r.aiter_lines():
                    if not line: continue
                    if line.startswith('data:'):
                        try:
                            # 這是 LangBot 核心的解析邏輯
                            data = json.loads(line[5:])
                            if 'data' in data and 'outputs' in data['data']:
                                outputs = data['data']['outputs']
                                for key in outputs:
                                    if isinstance(outputs[key], str):
                                        val = strip_xml_tags(outputs[key])
                                        if val: final_answer = val
                                        print(f"收到輸出 [{key}]: {val}")
                        except Exception as e:
                            print(f"解析 Line 失敗: {e}")
                
                print("\n================== 最終淨化結果 ==================")
                print(final_answer if final_answer else "警告: 輸出的 Outputs 欄位中沒有找到內容")
                print("==================================================")

        except Exception as e:
            print(f"連線/串流發生異常: {e}")

if __name__ == "__main__":
    asyncio.run(test_langbot_logic())
