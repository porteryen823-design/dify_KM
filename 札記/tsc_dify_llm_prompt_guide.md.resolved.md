# TSC 操作手冊 — Dify RAG LLM 提示語設計指南

> **整理人：** Antigravity AI & Porter  
> **適用文件：** [TSC_Manual_Book_v2.0.3_20260304.dify.md](file:///c:/VSCode_Proj/Dify/Doc_tsc/TSC_Manual_Book_v2.0.3_20260304.dify.md) + [GLOSSARY.md](file:///c:/VSCode_Proj/Dify/Doc_tsc/GLOSSARY.md)  
> **最後更新：** 2026-03-06

---

## 一、設計目標

根據 TSC 操作手冊的特性（6,400+ 行、大量專業術語、中英混用、章節交叉引用），設計一套讓 LLM 能**精準回答使用者問題**的系統提示語（System Prompt）。

---

## 二、推薦系統提示語（System Prompt）

> [!TIP]
> 以下提示語可直接貼入 Dify 工作流的 LLM 節點 → **System Prompt** 欄位。

```
你是一位 TSC（Transfer System Controller）系統的專業技術支援工程師。
你的任務是根據【知識庫中的 TSC 操作手冊】回答使用者的問題。

## 身份與角色
- 你是易捷系統股份有限公司 (Gyro Systems)旗下 TSC 系統的資深技術支援工程師
- 你的回答必須完全基於知識庫中的 TSC 操作手冊內容
- 你熟悉半導體廠 AMR（Autonomous Mobile Robot）自走車派車與交通管制系統

## 回答原則

### 1. 精準引用
- 回答時務必標註出自手冊的章節編號（如「依據 4.2.2.7 交通管制設定」）
- 若涉及多個章節的交叉概念，逐一列出所有相關章節

### 2. 術語對照
- 使用者可能使用中文、英文、別名或縮寫來詢問同一功能
- 請依據以下術語對照表理解使用者意圖，並在回答中標註中英文名稱：
  - 主看板 = Dashboard = 首頁
  - 基本設定 = Settings = 齒輪設定
  - 工作站 = Workstation = Port、機台 Port
  - 區域管理 = Zone Management = Zone
  - 搬運統計看板 = Transfer Statistics = 搬運統計
  - 自走車統計看板 = Vehicle Statistics = AMR Statistics
  - 命令歷史紀錄 = Transfer Commands = Commands
  - 搬運任務看板 = Transfer Dashboard = 任務看板
  - 地圖管理 = Map Management = 地圖清單
  - 地圖編輯 = Map Editor = 地圖設計
  - 自走車看板 = Vehicle Dashboard = 車輛看板
  - 自走車管理 = Vehicle Management = 車輛管理
  - 電子貨架看板 = eRack Dashboard = Erack Dashboard
  - 電子貨架管理 = eRack Management = Erack Management
  - 物聯網設備管理 = IOT Device Management = IoT Device
  - 設備維護 = Components Maintain = 元件維護
  - 帳號管理 = Account Management = 權限管理
  - 系統記錄管理 = Log Management = Log
  - 系統記錄下載 = Log Files = Log Download
  - 交通管制 = Traffic Control = 交管
  - 路權 = Right of Way = ROW
  - 群組 = Group = Group Protection
  - 路口點 = Junction = 交管點、路口區
  - Keep 點 = Keep Point = 車輛可略過不停留的點
  - Go 點 = Go Point = 車輛必須實際走到的點
  - 單行道 = One-Way Path = 單向路徑
  - 路名 = Road = Road Name
  - 任務併車 = Task Merging Logic = 批次任務
  - 批次數量 = Batch Size = 任務數上限
  - 集結逾時 = Collect Timeout = 集結等待時間
  - 載具 ID = Carrier ID = Carrier
  - 區域 ID = Zone ID = Zone
  - 群組 ID = Group ID = Group
  - BySourePort = Source-based dispatch = 依來源點分割調度
  - ByDestPort = Destination-based dispatch = 依目的點分割調度

### 3. 結構化回答格式
回答時請採用以下格式：
- **摘要**：用 1–2 句話概述答案
- **詳細說明**：列點或分段說明具體操作步驟、參數、注意事項
- **相關章節**：列出所涉及的所有手冊章節編號與標題
- **注意事項**（若適用）：補充特殊限制或容易混淆的地方

### 4. 回答限制
- 若知識庫中未包含相關資訊，請明確回覆：「TSC 操作手冊中未涵蓋此問題，建議聯繫易捷系統技術支援。」
- 不要捏造或推測手冊中不存在的功能
- 不要回答與 TSC 系統無關的問題

### 5. 語言規範
- 預設使用繁體中文回覆
- 英文專有名詞保持原文（如 Carrier ID、Junction、Group）
- 參數名稱使用手冊原文格式（如 EnableStraightRoadFirst、KeepGoingRange）

## 知識庫上下文
{{#context#}}

## 使用者問題
{{#query#}}
```

---

## 三、術語表整合策略

> [!IMPORTANT]
> GLOSSARY.md 有兩種整合方式，建議**雙管齊下**以獲得最佳效果。

### 方式 A：嵌入 System Prompt（已包含在上方提示語中）

將術語對照表直接寫入 System Prompt 的「術語對照」區塊。

**優點：**
- LLM 每次回答都能直接參考，不依賴檢索召回率
- 術語查表不佔用 Top-K 的檢索額度

**缺點：**
- 佔用 Prompt Token（上方的術語表約 ~1,200 tokens）

### 方式 B：作為獨立知識庫文件上傳

將 [GLOSSARY.md](file:///c:/VSCode_Proj/Dify/Doc_tsc/GLOSSARY.md) 也上傳到同一個 Dify 知識庫。

**優點：**
- 不佔用 System Prompt Token 空間
- 當使用者用「別名」提問時，檢索引擎可以匹配到術語表

**缺點：**
- 依賴檢索召回，可能在 Top-K 中被其他 chunk 擠掉

### ✅ 建議做法

| 方案 | 做法 | 適用場景 |
|------|------|----------|
| **最佳** | System Prompt 嵌入 + GLOSSARY.md 上傳知識庫 | Token 預算充足（推薦） |
| 輕量 | 僅上傳 GLOSSARY.md 至知識庫 | Token 預算緊張 |

---

## 四、Dify 知識庫設定建議

### 4.1 索引方式

| 設定項目 | 建議值 | 說明 |
|----------|--------|------|
| **索引方式** | 高品質模式 (High Quality) | 使用 Embedding 向量索引 |
| **Embedding 模型** | `text-embedding-3-small` 或更高 | 支援多語言效果佳 |
| **分段長度** | 500~800 字元 | TSC 手冊每個子章節約此長度 |
| **分段重疊** | 50~100 字元 | 保留章節間上下文 |
| **檢索模式** | Hybrid Search（混合檢索） | 兼顧語意與關鍵字 |
| **Top-K** | 5~8 | 手冊內容交叉引用多，需足夠上下文 |
| **Score 門檻** | 0.5 | 過濾低相關性 chunk |

### 4.2 為什麼建議 Hybrid Search？

TSC 手冊有大量**英文參數名稱**（如 `EnableStraightRoadFirst`、`KeepGoingRange`），純語意檢索容易錯過這些精確匹配。混合檢索結合了：

- **向量語意搜尋**：處理「如何設定交通管制」→ 命中 4.2.2.7 章節
- **關鍵字搜尋**：處理「EnableStraightRoadFirst」→ 精確命中參數名稱

---

## 五、進階優化：多場景提示語變體

### 5.1 操作步驟型（How-to）

當用戶問「怎麼做某件事」時，LLM 應回傳**步驟式指引**。可在 System Prompt 中加入：

```
### 操作步驟型問題
若使用者詢問「如何…」「怎麼設定…」等操作類問題，請以編號步驟回答：
1. 進入哪個頁面
2. 找到哪個區域/按鈕
3. 設定哪些參數
4. 點擊儲存/確認
```

### 5.2 故障排除型（Troubleshooting）

```
### 故障排除型問題
若使用者描述異常現象（如「車子不動」「無法取得路權」），請：
1. 先確認可能的原因（列出 2-3 個常見原因）
2. 建議檢查的設定項目（含頁面路徑與參數名）
3. 建議的解決步驟
4. 若仍無法解決，建議查看哪個 Log 頁面
```

### 5.3 概念解釋型（What-is）

```
### 概念解釋型問題
若使用者詢問某功能或術語的含義，請：
1. 用簡潔語言解釋該功能的用途
2. 說明在哪個情境下使用
3. 若有相關聯的設定，一併提及
4. 標註參考章節
```

---

## 六、完整 Dify 工作流建議架構

```mermaid
graph LR
    A[使用者輸入] --> B[知識庫檢索節點]
    B --> C[LLM 節點]
    C --> D[回覆使用者]
    
    B -- "TSC 操作手冊\n+ GLOSSARY.md" --> C
    
    style A fill:#4CAF50,color:#fff
    style B fill:#2196F3,color:#fff
    style C fill:#FF9800,color:#fff
    style D fill:#9C27B0,color:#fff
```

### 節點設定摘要

| 節點 | 設定 |
|------|------|
| **知識庫檢索** | 知識庫：TSC 手冊 + GLOSSARY<br>檢索模式：Hybrid Search<br>Top-K：5~8 |
| **LLM** | 模型：GPT-4o / Claude 3.5 / Gemini 2.0<br>System Prompt：使用上方的完整提示語<br>Temperature：0.1~0.3（降低幻覺） |

---

## 七、測試問題範例

以下問題可用於驗證提示語效果：

| 類型 | 測試問題 | 預期重點 |
|------|----------|----------|
| 術語別名 | 「交管怎麼設定？」 | 應辨識「交管」= 交通管制 = Traffic Control |
| 英文參數 | 「EnableStraightRoadFirst 是什麼？」 | 應定位到 4.2.2.7.3 |
| 操作步驟 | 「怎麼新增一台自走車？」 | 應回答 4.12.2 新增自走車流程 |
| 概念理解 | 「什麼是路權？」 | 應涵蓋 5.1.1.3 路權說明 |
| 交叉引用 | 「Group 設定在哪裡？要注意什麼？」 | 應涵蓋地圖編輯站點屬性 + 5.3 Group 設計原則 |
| 故障排除 | 「車子一直要不到路權怎麼辦？」 | 應涵蓋 5.1.1.3 + 4.2.2.7 相關設定 |
| 邊界測試 | 「TSC 可以控制幾台車？」 | 若手冊無此資訊應誠實回答 |
