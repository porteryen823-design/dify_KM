from __future__ import annotations

import httpx
import typing
import json
import re
import sys
from pathlib import Path
import os

from .errors import DifyAPIError

class AsyncDifyServiceClient:
    api_key: str
    base_url: str

    def __init__(self, api_key: str, base_url: str = 'https://api.dify.ai/v1') -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')

    async def chat_messages(
        self,
        inputs: dict[str, typing.Any],
        query: str,
        user: str,
        response_mode: str = 'streaming',
        conversation_id: str | None = None,
        files: list[dict[str, typing.Any]] = [],
        timeout: float = 300.0,
    ) -> typing.AsyncGenerator[dict[str, typing.Any], None]:
        payload = {
            'inputs': inputs,
            'query': query,
            'user': user,
            'response_mode': response_mode,
            'files': files
        }
        if conversation_id:
            payload['conversation_id'] = conversation_id
            
        print(f"DEBUG: Starting Dify stream to {self.base_url}/chat-messages (timeout={timeout})", file=sys.stderr, flush=True)
        async with httpx.AsyncClient(
            base_url=self.base_url,
            trust_env=True,
            timeout=httpx.Timeout(timeout, read=None),
        ) as client:
            try:
                async with client.stream(
                    'POST',
                    'chat-messages',
                    headers={'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'},
                    json=payload,
                ) as r:
                    print(f"DEBUG: Status={r.status_code}", file=sys.stderr, flush=True)
                    async for chunk_line in r.aiter_lines():
                        if not chunk_line: continue
                        print(f"DEBUG CHUNK: {chunk_line}", file=sys.stderr, flush=True)
                        if chunk_line.startswith('data:'):
                            try:
                                data = json.loads(chunk_line[5:])
                                yield data
                            except Exception as e:
                                print(f"DEBUG JSON Parse Error: {e}", file=sys.stderr, flush=True)
            except Exception as e:
                print(f"DEBUG EXCEPTION: {e}", file=sys.stderr, flush=True)

    async def upload_file(self, *args, **kwargs):
        pass

    async def workflow_run(
        self,
        inputs: dict[str, typing.Any],
        user: str,
        response_mode: str = 'streaming',
        files: list[dict[str, typing.Any]] = [],
        timeout: float = 300.0,
    ) -> typing.AsyncGenerator[dict[str, typing.Any], None]:
        print(f"DEBUG: Starting Dify stream to {self.base_url}/workflows/run (timeout={timeout})", file=sys.stderr, flush=True)
        async with httpx.AsyncClient(
            base_url=self.base_url,
            trust_env=True,
            timeout=httpx.Timeout(timeout, read=None),
        ) as client:
            try:
                async with client.stream(
                    'POST',
                    'workflows/run',
                    headers={'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'},
                    json={'inputs': inputs, 'user': user, 'response_mode': response_mode, 'files': files},
                ) as r:
                    print(f"DEBUG: Status={r.status_code}", file=sys.stderr, flush=True)
                    async for chunk_line in r.aiter_lines():
                        if not chunk_line: continue
                        print(f"DEBUG CHUNK: {chunk_line}", file=sys.stderr, flush=True)
                        if chunk_line.startswith('data:'):
                            try:
                                data = json.loads(chunk_line[5:])
                                yield data
                            except Exception as e:
                                print(f"DEBUG JSON Parse Error: {e}", file=sys.stderr, flush=True)
            except Exception as e:
                print(f"DEBUG EXCEPTION: {e}", file=sys.stderr, flush=True)
