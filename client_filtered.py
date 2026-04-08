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
        # Ensure base_url ends correctly for relative pathing (handled in stream)
        self.base_url = base_url.rstrip('/')

    def _strip_xml_tags(self, text: str) -> str:
        """移除 <think> 和 <context> 等常見 XML 標籤內容"""
        # 移除 <think>...</think> 及其內容
        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        # 移除 <context>...</context> 及其內容 (或只移除標籤保留內容)
        text = re.sub(r'<context>|</context>', '', text)
        return text.strip()

    async def chat_messages(
        self,
        inputs: dict[str, typing.Any],
        query: str,
        user: str,
        response_mode: str = 'streaming',
        conversation_id: str = '',
        files: list[dict[str, typing.Any]] = [],
        timeout: float = 30.0,
        model_config: dict[str, typing.Any] | None = None,
    ) -> typing.AsyncGenerator[dict[str, typing.Any], None]:
        if response_mode != 'streaming':
            raise DifyAPIError('当前仅支持 streaming 模式')

        async with httpx.AsyncClient(
            base_url=self.base_url,
            trust_env=True,
            timeout=timeout,
        ) as client:
            payload = {
                'inputs': inputs, 'query': query, 'user': user,
                'response_mode': response_mode, 'conversation_id': conversation_id,
                'files': files, 'model_config': model_config or {},
            }

            async with client.stream(
                'POST',
                'chat-messages',
                headers={'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'},
                json=payload,
            ) as r:
                async for chunk in r.aiter_lines():
                    if r.status_code != 200: raise DifyAPIError(f'{r.status_code} {chunk}')
                    if chunk.strip() == '': continue
                    if chunk.startswith('data:'):
                        data = json.loads(chunk[5:])
                        if 'answer' in data:
                            data['answer'] = self._strip_xml_tags(data['answer'])
                        yield data

    async def workflow_run(
        self,
        inputs: dict[str, typing.Any],
        user: str,
        response_mode: str = 'streaming',
        files: list[dict[str, typing.Any]] = [],
        timeout: float = 30.0,
    ) -> typing.AsyncGenerator[dict[str, typing.Any], None]:
        if response_mode != 'streaming':
            raise DifyAPIError('当前仅支持 streaming 模式')

        print(f"DEBUG: Request to: {self.base_url}/workflows/run")
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
                print(f"DEBUG: Status: {r.status_code}")
                async for chunk in r.aiter_lines():
                    if r.status_code != 200: raise DifyAPIError(f'{r.status_code} {chunk}')
                    if chunk.strip() == '': continue
                    if chunk.startswith('data:'):
                        data = json.loads(chunk[5:])
                        # 處理 Workflow 的輸出過濾
                        if 'data' in data and 'outputs' in data['data']:
                            for key in data['data']['outputs']:
                                if isinstance(data['data']['outputs'][key], str):
                                    data['data']['outputs'][key] = self._strip_xml_tags(data['data']['outputs'][key])
                        yield data

    async def upload_file(
        self,
        file: httpx._types.FileTypes,
        user: str,
        timeout: float = 30.0,
    ) -> str:
        if isinstance(file, Path):
            with open(file, 'rb') as f: file = f.read()
        elif isinstance(file, str):
            with open(file, 'rb') as f: file = f.read()
        elif hasattr(file, 'read'):
            file = file.read()
        async with httpx.AsyncClient(base_url=self.base_url, trust_env=True) as client:
            response = await client.post(
                'files/upload',
                headers={'Authorization': f'Bearer {self.api_key}'},
                files={'file': file}, data={'user': (None, user)},
            )
            if response.status_code != 201: raise DifyAPIError(f'{response.status_code} {response.text}')
            return response.json()
