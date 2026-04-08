from __future__ import annotations

import httpx
import typing
import json
import re

from .errors import DifyAPIError
from pathlib import Path
import os


class AsyncDifyServiceClient:
    """Dify Service API 客户端"""

    api_key: str
    base_url: str

    def __init__(
        self,
        api_key: str,
        base_url: str = 'https://api.dify.ai/v1',
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')

    def _strip_xml_tags(self, text: str) -> str:
        """移除 <think> 和 <context> 等常見 XML 標籤內容"""
        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        text = re.sub(r'<context>|</context>', '', text)
        return text.strip()

    async def workflow_run(
        self,
        inputs: dict[str, typing.Any],
        user: str,
        response_mode: str = 'streaming',
        files: list[dict[str, typing.Any]] = [],
        timeout: float = 300.0,
    ) -> typing.AsyncGenerator[dict[str, typing.Any], None]:
        """運行並彙整工作流"""
        print(f"DEBUG: Active to: {self.base_url}/workflows/run (300s timeout)")
        async with httpx.AsyncClient(
            base_url=self.base_url,
            trust_env=True,
            timeout=timeout,
        ) as client:
            async with client.stream(
                'POST',
                'workflows/run',
                headers={'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'},
                json={'inputs': inputs, 'user': user, 'response_mode': response_mode, 'files': files},
            ) as r:
                async for chunk_line in r.aiter_lines():
                    if r.status_code != 200: raise DifyAPIError(f'{r.status_code} {chunk_line}')
                    if not chunk_line or not chunk_line.startswith('data:'): continue
                    
                    data = json.loads(chunk_line[5:])
                    # 關鍵：為了讓 LangBot 把回傳當成「答案」，我們要把 outputs 包進一個 answer 假欄位
                    # 如果是 workflow_finished，我們把它的 outputs 傳出去
                    if data.get('event') == 'workflow_finished':
                        outputs = data.get('data', {}).get('outputs', {})
                        for k, v in outputs.items():
                            if isinstance(v, str):
                                clean_val = self._strip_xml_tags(v)
                                # 這是 LangBot 預期收到的格式：
                                yield {'event': 'message', 'answer': clean_val, 'metadata': data}
                    
                    # 同步輸出中間過程（如果有的話）
                    yield data

    async def chat_messages(self, *args, **kwargs):
        # 這裡同樣實作 XML 標籤移除邏輯 (略)
        pass

    async def upload_file(self, *args, **kwargs):
        pass
