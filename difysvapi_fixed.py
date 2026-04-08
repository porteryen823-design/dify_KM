import json
import typing
import uuid
import re

from ...pipeline import query as pipeline_query
from .. import message as provider_message
from ...utils import importutil
from . import base, errors


class DifyServiceAPI(base.Provider):
    # ... (簡化，只顯示核心修正部分，我會用 sed 或整個覆蓋)
    async def _workflow_messages_chunk(self, query: pipeline_query.Query):
        # ... 
        async for chunk in self.dify_client.workflow_run(...):
            if chunk['event'] == 'workflow_finished':
                # 這裡就是修正點：Dify Workflow 的結果在 outputs 裡！
                outputs = chunk['data'].get('outputs', {})
                # 遍歷所有 output，找到第一個非空的文字內容
                for val in outputs.values():
                    if isinstance(val, str) and val.strip():
                        workflow_contents = val # 抓取結果
                        break
                is_final = True
            # ...
