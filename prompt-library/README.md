# AUTOMAT Prompt Library 知識庫系統

> **整理人：** Antigravity AI & Porter
>
> **建立日期：** 2026-03-12
>
> **用途：** 提供企業級 AUTOMAT Prompt 範例查詢服務，並與 Dify Chatbot 深度整合。

---

## 一、專案概述

本專案旨在建立一個結構化的 **Prompt Library**，儲存超過 30 個遵循 **AUTOMAT 框架** 的高品質提示語範例。透過 FastAPI 後端與 Dify Chatbot 的整合，使用者可以利用自然語言直接搜尋並獲取適合其業務情境（如 HR、行銷、IT 等）的 Prompt 範本。

### 核心價值
*   **標準化**：統一採用 AUTOMAT (Actor, User, Task, Output, Method, Assumption, Tone) 框架。
*   **即時性**：Dify Chatbot 透過 API 即時檢索資料庫，確保範例最新且可隨時擴充。
*   **多樣化**：涵蓋 HR、Marketing、IT、Sales、Ops、Strategy 六大領域。

---

## 二、系統架構

```
使用者互動介面 (Dify Chatbot)
      │
[Intent Analysis] (LLM) ── 識別使用者關鍵字
      │
[HTTP Request] (Dify Tool) ── 呼叫 Backend API
      │
[FastAPI Service] (Python) ── 業務邏輯處理
      │
[SQLite Database] ── 儲存 30+ 筆範例資料
```

---

## 三、技術棧 (Technology Stack)

本專案遵循 **Profile A：前後端分離** 的技術規範。

*   **後端框架**：FastAPI (Python 3.11+)
*   **資料庫**：SQLite (在地化輕量資料庫)
*   **整合平台**：Dify 0.6.0+ (Advanced Chat Workflow)
*   **模型**：minimax-m2.5:cloud (用於意圖分析與結果格式化)

---

## 四、資料庫設計 (Database Schema)

### Table: `PromptLibrary`

| 欄位 (Column) | 型別 | 說明 |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary Key, Auto-increment |
| `category` | TEXT | 領域分類 (HR / Marketing / IT / Ops / Sales / Strategy) |
| `name` | TEXT | Prompt 名稱 |
| `description` | TEXT | 用途與場景描述 |
| `actor` | TEXT | AUTOMAT: 角色 (Actor) |
| `user_audience`| TEXT | AUTOMAT: 目標對象 (User) |
| `task` | TEXT | AUTOMAT: 任務 (Task) |
| `output` | TEXT | AUTOMAT: 輸出格式 (Output) |
| `method` | TEXT | AUTOMAT: 方法 (Method) |
| `assumption` | TEXT | AUTOMAT: 假設條件 (Assumption) |
| `tone` | TEXT | AUTOMAT: 語氣風格 (Tone) |
| `example` | TEXT | 完整的 Markdown 範例內容 |
| `tags` | TEXT | 搜尋用標籤 (逗號分隔) |

---

## 五、API 端點說明 (API Endpoints)

服務運行於預設端口：`8005`

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/prompts` | 取得清單，支援 `category` 篩選 |
| `GET` | `/prompts/search` | **關鍵字搜尋**，支援 `q` 參數（全文檢索名稱、描述與標籤） |
| `GET` | `/prompts/{id}` | 取得特定 ID 的詳細範例內容 |

### 範例請求
```bash
curl "http://localhost:8005/prompts/search?q=HR"
```

---

## 六、Dify 整合流程 (Workflow Nodes)

更新後的 DSL (`automat-prompt-library.yml`) 包含以下核心節點：

1.  **意圖分析 (LLM Node)**：萃取使用者對話中的領域關鍵字。
2.  **搜尋知識庫 (HTTP Request Node)**：動態傳遞關鍵字至 API 並接收 JSON 結果。
3.  **範例展示 (LLM Node)**：根據 API 回傳值，利用 AUTOMAT 指南對結果進行格式化輸出。

---

## 七、環境安裝與執行

### 1. 後端服務啟動
```powershell
cd c:\VSCode_Proj\Dify\prompt-library
# 建立虛擬環境
python -m venv venv
.\venv\Scripts\activate
# 安裝依賴
pip install -r requirements.txt
# 初始化資料庫 (執行一次即可)
python scripts/seed_db.py
# 啟動 API
uvicorn src.main:app --host 0.0.0.0 --port 8005
```

### 2. Dify DSL 匯入
將 `c:\VSCode_Proj\Dify\DSL\automat-prompt-library.yml` 匯入 Dify 平台即可開始測試。

---

## 八、版本規範 (Versioning)

*   **V0.1**：初始版本，建立 30 筆範本庫與基本 API。
*   **V0.2**：整合 Dify Workflow，實現意圖驅動的範例搜尋。
