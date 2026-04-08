---
description: 在 Dify DSL 中加入清理 LLM `<think>` 標籤的 Code 節點 (LLM -> Code -> Answer)
---
# Dify DSL 增加清理思維標籤節點

這個 workflow 的目的是在 Dify 的 Chatflow 或 Workflow 中，當使用具備推理能力（Reasoning）的 LLM（例如 Ollama 模型、DeepSeek R1 等）時，自動將 `<think>...</think>` 思維鏈標籤從最終輸出中移除，避免直接呈現給使用者。

## 適用情境
- LLM 節點輸出的結構會帶有 `<think>` 標籤。
- 最終 Answer 節點需要直接展示訊息給使用者，但不應顯示推論過程。
- 原本的處理鏈是：`LLM 節點` → `Answer 節點`。

## 處理步驟

### 1. 修改原有的 Edge
將原本連接 `LLM 節點` 到 `Answer 節點` 的 Edge 打斷，改為指向我們新建的 Code 節點 (`code_clean_answer`)：

```yaml
    - data:
        isInIteration: false
        sourceType: llm
        targetType: code
      id: edge-llm-to-clean
      source: <YOUR_LLM_NODE_ID>
      sourceHandle: source
      target: code_clean_answer
      targetHandle: target
      type: custom
```

### 2. 新增 Edge：Code -> Answer
新增一條 edge，把新的 Code 節點連接到原本的 Answer 節點：

```yaml
    - data:
        isInIteration: false
        sourceType: code
        targetType: answer
      id: edge-code-clean-to-answer
      source: code_clean_answer
      sourceHandle: source
      target: <YOUR_ANSWER_NODE_ID>
      targetHandle: target
      type: custom
```

### 3. 加入 Code 節點配置 (code_clean_answer)
在 `nodes` 陣列中新增清洗邏輯的 Code 節點。這段 Python 腳本會處理輸入的字串去除包括 `<think>` 在內的標籤內容。
**注意：** 記得要把 `<YOUR_LLM_NODE_ID>` 改成實際 LLM 節點的 ID。

```yaml
    - data:
        code: "import re\ndef main(llm_text: str) -> dict:\n    cleaned = re.sub(r'<think>.*?</think>',\\\n      \\ '', llm_text, flags=re.DOTALL).strip()\n    return {\"cleaned_text\": cleaned}"
        code_language: python3
        desc: 移除 LLM 輸出中的 <think>...</think> 思維鏈標籤
        outputs:
          cleaned_text:
            children: null
            type: string
        selected: false
        title: 清理思維標籤
        type: code
        variables:
        - value_selector:
          - <YOUR_LLM_NODE_ID>
          - text
          variable: llm_text
      height: 96
      id: code_clean_answer
      position:
        x: 1000  # 請根據前後節點調整座標
        y: 120
      positionAbsolute:
        x: 1000
        y: 120
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 242
```

### 4. 更新 Answer 節點的變數引用
將目標 Answer 節點中原本引用的 LLM 結果（如 `{{#<YOUR_LLM_NODE_ID>.text#}}`），修改為引用我們 Code 節點輸出的 `cleaned_text`：

```yaml
    - data:
        answer: '{{#code_clean_answer.cleaned_text#}}'
        # 保留原有的其他設定...
```

完成這四個步驟後，對應的 Chatflow/Workflow 就不會再把 `<think>` 推理內容原封不動地渲染到前端介面了。
