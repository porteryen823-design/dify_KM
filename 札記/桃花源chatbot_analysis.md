# 桃花源 Knowledge Retrieval + Chatbot — 分析與修正報告

> **整理人：** Antigravity AI & Porter  
> **最後更新：** 2026-03-06

---

## 一、Chatbot 架構理解

此 Dify 應用為 **Advanced Chat（進階聊天）** 模式，工作流架構如下：

```mermaid
graph LR
    A["Start"] --> B["Knowledge Retrieval"]
    B --> C["LLM"]
    C --> D["Answer"]
    
    style A fill:#4CAF50,color:#fff
    style B fill:#2196F3,color:#fff
    style C fill:#FF9800,color:#fff
    style D fill:#9C27B0,color:#fff
```

| 節點 | 功能 | 目前設定 |
|------|------|----------|
| **Start** | 接收使用者輸入 | 無自訂變數 |
| **Knowledge Retrieval** | 從知識庫檢索相關段落 | 混合檢索、Top-K=2、Reranking 關閉 |
| **LLM** | 使用大語言模型生成回答 | `gpt-oss:20b` via Ollama、temperature=0.1 |
| **Answer** | 回傳 LLM 輸出 | 直接輸出 `{{#LLM.text#}}` |

---

## 二、發現的問題

### 🔴 嚴重問題

| # | 問題 | 影響 |
|---|------|------|
| 1 | **System Prompt 過於通用** | 完全沒有針對「桃花源記」定義角色和回答策略，LLM 無法發揮文學分析能力 |
| 2 | **`suggested_questions` 為空** | 使用者進入對話後沒有引導，不知道該問什麼 |
| 3 | **`retriever_resource.enabled: false`** | 使用者看不到 LLM 回答時引用了哪些知識庫段落，降低可信度 |

### 🟡 中度問題

| # | 問題 | 影響 |
|---|------|------|
| 4 | **Knowledge Retrieval `top_k: 2` 太低** | 僅取回 2 個段落，桃花源記有原文、註釋、賞析等多種段落，容易遺漏重要內容 |
| 5 | **LLM `temperature: 0.1` 過低** | 回答會過於僵硬死板，文學鑑賞需要一定的創意和表達自由度 |
| 6 | **LLM `top_p: 0.4` 過低 + `top_k: 1` 過低** | 與 temperature 疊加，使回答範圍極度受限 |
| 7 | **Memory（對話記憶）關閉** | 無法進行多輪深入討論，使用者問了上一個問題後，LLM 會「失憶」 |

### 🟢 建議改善

| # | 內容 |
|---|------|
| 8 | **Opening Statement** 太簡單，缺乏引導性和親和力 |
| 9 | **Reranking 建議開啟**，可提升檢索結果的精準度 |

---

## 三、修正內容

### 3.1 改善的 System Prompt

```
你是一位精通中國古典文學的桃花源記研究助手。

## 身份與角色
- 你是一位專攻魏晉文學、尤其對陶淵明及《桃花源記》有深入研究的文學助手
- 你的回答必須基於知識庫中提供的原文與相關資料
- 你能夠協助使用者理解文言文字詞、文學意涵、寫作手法與歷史背景

## 知識庫上下文
<context>
{{#context#}}
</context>

## 回答原則

### 1. 原文引用
- 回答時盡量引用《桃花源記》的原文段落，用引號「」標示
- 若涉及特定情節，指出該段落在原文中的位置

### 2. 文言文詞語解釋
- 遇到文言文字詞時，提供白話文翻譯
- 例如：「阡陌交通」→ 田間小路交錯相通
- 重要字詞提供詞義辨析

### 3. 結構化回答格式
回答時採用以下格式：
- **簡要回答**：用 1-2 句話概述核心答案
- **詳細分析**：展開論述，引用原文佐證
- **延伸思考**（若適用）：提供相關的文學或歷史延伸知識

### 4. 回答限制
- 若知識庫中未包含相關資訊，請誠實告知：「目前資料中未涵蓋此問題，建議參考其他文學資料。」
- 不要編造不存在於原文中的情節或解讀
- 可以提供學術界的主流觀點，但需註明有不同解讀的可能

### 5. 語言規範
- 使用繁體中文回答
- 原文引用保留文言文原貌
- 語氣親切但專業，像一位熱情的文學老師

### 6. 多角度分析
當討論文學意涵時，可從以下角度切入：
- 歷史背景（東晉時代）
- 作者生平（陶淵明的隱逸精神）
- 文學手法（象徵、對比、空間描寫）
- 哲學思想（道家、儒家、烏托邦理想）
```

### 3.2 改善的 Opening Statement

```
你好！🌸 我是桃花源記的文學助手。

我可以幫你深入理解陶淵明的《桃花源記》，包括：
📖 原文字詞解釋與白話翻譯
🎨 文學手法與寫作特色分析
🏛️ 歷史背景與作者思想探討
💭 文學意涵與哲學思考

請隨意提問，讓我們一起走進那片「芳草鮮美，落英繽紛」的世外桃源！
```

### 3.3 對話開場白建議問題（Suggested Questions）

經過搜尋與分析，以下 5 個問題涵蓋不同面向，適合作為對話開場白：

| # | 建議問題 | 涵蓋面向 |
|---|----------|----------|
| 1 | 🏞️「桃花源中的居民為何『不知有漢，無論魏晉』？這說明了什麼？」 | 原文理解 + 深層含義 |
| 2 | ✍️「陶淵明為何要寫《桃花源記》？與他所處的時代有什麼關係？」 | 歷史背景 + 創作動機 |
| 3 | 🔍「漁人離開後為何再也找不到桃花源？結尾有什麼寓意？」 | 情節分析 + 文學意涵 |
| 4 | 📝「桃花源記使用了哪些文學手法來描繪理想世界？」 | 寫作技巧 + 文學鑑賞 |
| 5 | 🤔「桃花源可以算是中國版的『烏托邦』嗎？兩者有何異同？」 | 比較文學 + 哲學思辨 |

> [!TIP]
> Dify `suggested_questions` 最多建議放 **3~5 個**，太多會讓介面擁擠。上面 5 個可擇優選取。

### 3.4 LLM 參數調整

| 參數 | 原值 | 建議值 | 說明 |
|------|------|--------|------|
| `temperature` | 0.1 | **0.4** | 文學回答需要一定表達自由度，但不能太高以免胡說 |
| `top_k` | 1 | **5** | 擴大候選詞彙範圍，讓回答更自然 |
| `top_p` | 0.4 | **0.7** | 提升表達多樣性 |

### 3.5 Knowledge Retrieval 參數調整

| 參數 | 原值 | 建議值 | 說明 |
|------|------|--------|------|
| `top_k` | 2 | **4~5** | 取回更多相關段落，避免遺漏 |
| `reranking_enable` | false | **true** | 開啟二次排序，提升召回品質 |

### 3.6 Features 調整

| 設定 | 原值 | 建議值 | 說明 |
|------|------|--------|------|
| `retriever_resource.enabled` | false | **true** | 顯示引用來源，提升可信度 |
| `memory.window.enabled` | false | **true** | 開啟對話記憶 |
| `memory.window.size` | 50 | **10** | 保留最近 10 輪對話 |

---

## 四、修正後完整 DSL 變動摘要

以下為完整的修改清單（請在 DSL 中對應修改）：

```diff
  features:
-   opening_statement: 你好! 歡迎使用 桃花源記問題 小幫手!
+   opening_statement: "你好！🌸 我是桃花源記的文學助手。\n\n我可以幫你深入理解陶淵明的《桃花源記》，包括：\n📖 原文字詞解釋與白話翻譯\n🎨 文學手法與寫作特色分析\n🏛️ 歷史背景與作者思想探討\n💭 文學意涵與哲學思考\n\n請隨意提問，讓我們一起走進那片「芳草鮮美，落英繽紛」的世外桃源！"
    retriever_resource:
-     enabled: false
+     enabled: true
-   suggested_questions: []
+   suggested_questions:
+     - '桃花源中的居民為何「不知有漢，無論魏晉」？這說明了什麼？'
+     - '陶淵明為何要寫《桃花源記》？與他所處的時代有什麼關係？'
+     - '漁人離開後為何再也找不到桃花源？結尾有什麼寓意？'
```

```diff
  # Knowledge Retrieval 節點
        multiple_retrieval_config:
-         reranking_enable: false
+         reranking_enable: true
-         top_k: 2
+         top_k: 5
```

```diff
  # LLM 節點
        model:
          completion_params:
-           temperature: 0.1
+           temperature: 0.4
-           top_k: 1
+           top_k: 5
-           top_p: 0.4
+           top_p: 0.7
```

```diff
  # LLM Memory
        memory:
          window:
-           enabled: false
+           enabled: true
-           size: 50
+           size: 10
```

```diff
  # LLM System Prompt（完整替換）
        prompt_template:
        - role: system
          text: |
            你是一位精通中國古典文學的桃花源記研究助手。
            ... (完整 prompt 見 3.1 節)
```

---

> [!IMPORTANT]
> 修正後的完整 DSL 檔案已另存為 [桃花源 Knowledge Retrieval + Chatbot .yml](file:///c:/VSCode_Proj/Dify/DSL/桃花源%20Knowledge%20Retrieval%20+%20Chatbot%20.yml)，可直接匯入 Dify 使用。
