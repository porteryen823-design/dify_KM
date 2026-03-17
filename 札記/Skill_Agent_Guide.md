# 📘 Dify Skill 生態開發與維護指南

> **整理人：** Antigravity AI & Porter

---

## 一、 環境基礎配置 (`.env`)

若要讓插件（Plugin）能正確處理檔案並在工作流中執行，Docker 環境變數必須設定為**絕對路徑**或**正確的內部地址**。

### 1. 外部存取 URL (瀏覽器使用)
這類變數必須指向 Nginx 的對外入口（預設 `8080`），否則網頁會卡在 Loading 或出現 CORS 錯誤。
*   `FILES_URL=http://localhost:8080`
*   `CONSOLE_API_URL=http://localhost:8080`
*   `CONSOLE_WEB_URL=http://localhost:8080`

### 2. 內部存取 URL (容器通訊使用) 🌟 **最重要**
這是解決 `Connection refused` 或 `unknown url type` 的關鍵。插件守護進程（`plugin_daemon`）必須透過 Docker 內部網路存取 API。
*   **`INTERNAL_FILES_URL=http://api:5001`**

---

## 二、 檔案上傳設定 (DSL 規範)

Dify 預設限制較嚴格。若要支援 Skill 的 ZIP 安裝或 Python 腳本上傳，必須在 DSL 的 `file_upload` 特性中開啟權限。

### 建議配置清單：
*   **允許副檔名**：增加 `.zip`, `.ZIP`, `.py`, `.txt`。
*   **允許檔案類型**：除了 `image`，務必開啟 **`document`** (ZIP 歸類在此)。
*   **大小寫敏感**：建議同時加入大寫與小寫（如 `.ZIP` 與 `.zip`）。

---

## 三、 節點異常排查 (`client-side exception`)

當點選工作流節點出現瀏覽器崩潰（Exception）時，通常是因為 DSL 匯入的模型或變數與當前環境不相符。

### 1. 模型缺失
*   **現象**：DSL 中的 `model` 指向了環境中不存在的服務（如舊的 `gpt-oss:20b`）。
*   **對策**：將 DSL 中的 `model.value` 暫時設為 `null`，重啟頁面後在 UI 手動重新選擇。

### 2. 參數綁定錯誤
*   **現象**：在 `tool_parameters` 中直接使用 `{{#sys.files#}}` 導致渲染失敗。
*   **對策**：將參數類型暫時改為 `constant` 且值為 `null`，待進入 UI 後再改回 `mixed` 並綁定變數。

---

## 四、 核心組件說明

### 1. Skill Manager (TM - Tool Manager)
*   **功能**：用於安裝（Add）、刪除（Delete）、查詢（List）技能。
*   **操作語義**：建議在 `IF 條件分支` 節點中包含關鍵字：`新增技能`、`查看技能`、`安裝`、`上傳`。
*   **檔案參數**：`files` 必須綁定 `{{#sys.files#}}`，否則會報錯「未檢測到 ZIP」。

### 2. Skill_Agent
*   **功能**：真正的執行大腦。它會根據您已安裝的「技能說明書（SKILL.md）」來調用 Python 腳本進行任務。
*   **重要參數**：
    *   `History turns`：控制上下文長度。
    *   `Max steps`：限制 Agent 思考深度（防止死循環）。
    *   `Query`：綁定為 `{{#sys.query#}}` 以接收使用者指令。

---

## 五、 資料儲存目錄 (宿主機)

所有資料都持久化在 Docker 目錄下，您可以直接備份此資料夾：
*   **位置**：`c:\VSCode_Proj\Dify\dify\docker\volumes\app\storage\`
*   **對應關係**：
    *   `plugin/`：Dify 官方/第三方插件包。
    *   `persistence/`：**Skill 實際安裝後的資料**與 Session 對話歷史。

---

## 七、 版本與相容性說明

為了確保系統穩定，請遵循以下版本基準：
*   **Dify 版本**：`1.13.0` (LangGenius 官方 Docker 映像檔)。
*   **Skill Agent 插件**：`lfenghx/skill_agent:0.0.3`。
*   **Python 執行環境**：插件內部使用 `Python 3.12`，開發程式碼時請確保語法相容。
*   **容器作業系統**：Alpine/Debian (Docker 內部)，安裝 Skill 時若有特殊作業系統依賴，請確認插件容器是否支援。

---

## 八、 核心注意事項

1.  **內外網址區分**：`FILES_URL` 給人用，`INTERNAL_FILES_URL` 給機器用。這兩者一旦混淆，檔案下載必敗。
2.  **設定生效方式**：修改 `.env` 後，不可僅下 `docker restart`。必須執行 **`docker-compose down && docker-compose up -d`** 才能重新讀取環境變數。
3.  **ZIP 套件結構**：ZIP 根目錄必須包含 `SKILL.md`，否則 Skill_Agent 會找不到可執行指令。
4.  **模型權限**：確保您在 Skill_Agent 中選擇的模型（如 minimax-m2.5）在對應的 Workspace 中已正確配置 API Key 且處於連連通狀態。
5.  **DSL 遷移風險**：由 A 環境匯出的 DSL 到 B 環境時，建議先移除模型配置，匯入後再重新選擇，以避免 `client-side exception`。

**整理人：** Antigravity AI & Porter
