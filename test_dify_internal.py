import httpx
import json

async def test():
    url = "http://nginx/v1/workflows/run"
    headers = {
        "Authorization": "Bearer app-dTIUOMtSVP75RYLKe4klIk3j",
        "Content-Type": "application/json"
    }
    data = {
        "inputs": {"query": "test"},
        "user": "debug-user",
        "response_mode": "blocking"
    }
    async with httpx.AsyncClient() as client:
        try:
            print(f"Testing {url}...")
            resp = await client.post(url, headers=headers, json=data, timeout=30.0)
            print(f"Status Code: {resp.status_code}")
            print(f"Response: {resp.text}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test())
