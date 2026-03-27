# Antigravity 通用工程規則（Rules）

> 本文件為 Antigravity 專案的**最終工程規範版本**，用於所有新專案與既有專案維護。
>
> 核心設計理念：
>
> * **單一專案只能啟用一種 Technology Profile**
> * 規則必須可落地、可自動化、可長期維護

---

## 一、語言與輸出約定

* 所有回覆、說明、註釋、文件,Walkthrough **必須使用繁體中文**
* 程式碼中的識別符（變數、函數、類別）一律使用英文
* 禁止使用拼音命名
* 錯誤訊息、例外、日誌、print 內容 **強制使用英文**
* **文件署名規範**：凡輸出文件中含有 `**整理人：** Antigravity AI`，一律改寫為 `**整理人：** Antigravity AI & Porter`，體現人機協作精神。

---

## 二、Technology Profiles（技術路線）

> ⚠️ **重要原則**：
>
> **一個專案只能選擇並遵循一個 Profile**，不可混用。 (Profile A | B | C | D | E | F | G | H | I | J)

---

## Profile A：前後端分離（預設）
### A-1 適用情境
* 傳統企業系統、微服務架構、高度客製後端商業邏輯。

---

## Profile B：Next.js 全端專案
### B-1 適用情境
* SaaS、MVP、快速驗證產品假設。

---

## Profile C：靜態簡易網頁（HTML + TailwindCSS + JavaScript）
### C-1 適用情境
* 單頁展示、Landing Page、無複雜後端邏輯。

---

## Profile D：Odoo 客製化開發
### D-1 適用情境
* ERP 系統客製化（強制使用 Odoo 17.0）。

---

## Profile E：Blazor 全端專案 (.NET + C#)
### E-1 適用情境
* 企業內部管理系統、高度依賴微軟生態系。

---

## Profile F：ASP.NET Core Web API 後端專案
### F-1 適用情境
* RESTful API 後端服務、微服務架構。

---

## Profile G：RAG (Retrieval-Augmented Generation) 知識庫系統
### G-1 適用情境
* 基於 LangChain 1.x LCEL 架構的知識庫問答。

---

## Profile H：Dify 生態系統開發
### H-1 適用情境
* Dify 平台核心開發、插件與擴展。DSL 工作流規範 (0.6.0)。

---

## Profile I：n8n 自動化流程與節點開發
### I-1 適用情境
* n8n 自定義節點與複雜工作流設計。

---

## Profile J：傳統伺服器渲染 (SSR) + 現代介面交互

### J-1 適用情境
* 快速原型開發或整合現有後端系統。
* 具備動態 API 代理需求 (如 Dify 整合)。
* 適合管理後台、內部工具或包含豐富前端動態交互 (AJAX) 的入口網站。

### J-2 技術棧
* **後端**: Python 3.10+ (Flask / FastAPI)
* **模板**: Jinja2
* **前端框架**: Bootstrap 5 (CDN 或 資源包)
* **前端邏輯**: Vanilla JavaScript (ES2022+)
* **樣式**: Custom CSS (支援現代美學：Glassmorphism, Dark Mode)

### J-3 專案目錄結構
```
project-root/
├─ app.py             # 核心邏輯與路由
├─ data/              # SQLite 庫與持久化檔案
├─ static/
│  ├─ css/            # 自定義樣式
│  ├─ js/             # 獨立 JS 邏輯
│  └─ img/
├─ templates/         # Jinja2 模板
│  ├─ base.html       # 基礎版面
│  └─ ...
├─ requirements.txt
└─ README.md
```

### J-4 設計與禁止事項
* **禁止** 在 HTML 內堆積過長 JS（>100 行應抽離）。
* **安全性**: 所有 API Key 必須由後端 Proxy 處理。

---

## 三、通用命名與程式碼規範

| 類型       | 規範               |
| -------- | ---------------- |
| 變數 / 函數  | camelCase        |
| 類別 / 元件  | PascalCase       |
| 常數       | UPPER_SNAKE_CASE |
| 檔案 / 資料夾 | kebab-case       |

---

## 四、流程與文件要求
* 複雜業務流程必須提供 **Mermaid 流程圖**。

---

## 五、專案宣告（必須）
每個 README.md 必須包含：
```md
## Project Profile
- Technology Profile: Profile A | ... | Profile J
```

---

## 八、Windows 環境特定規範
### 8-1 Unicode 輸出編碼處理
在 Windows 控制台執行時，必須在進入點加入：
```python
import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
```

---

## 九、版本控管 (Version Control Rules)
* **強制設定 .gitignore**：排除 `.env`, `node_modules`, `venv`, `__pycache__` 等。
* **分支命名**: `feature/`, `bugfix/`, `hotfix/`。

---

## 十、資料庫命名規範
* 資料表使用 **複數名詞** (如 `employees`)。
* 欄位使用 **單數名詞** (如 `employee_id`)。

---

## 十一、測試規範 (Testing Rules)
* 核心邏輯強制測試，採用 **AAA Pattern (Arrange-Act-Assert)**。

---

## 十二、日誌與錯誤處理
* **格式**: `[時間戳] 等級 模組名稱 - 訊息內容`。
* 禁止使用裸 `try-except`。

---

## 十六、Excel 操作規範
* **強制** 使用 `excel-mcp-server`。
* 表頭應設定為 **粗體** 搭配 **藍色背景**。

---

## 十七、LLM 模型規範
* **預設模型 (Default Model)**：除非專案另有明確指明（如需使用 GPT-4o 進行複雜分析），否則所有 Dify 應用、Agent 或推理腳本的預設 LLM 一律使用 **`gpt-oss:20b`** (Ollama)。

**整理人：** Antigravity AI & Porter
