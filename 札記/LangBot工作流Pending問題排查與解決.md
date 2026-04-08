# LangBot 整合 Dify 工作流「Pending」問題排查與解決

> **建立日期：** 2026-04-08
> **整理人：** Antigravity AI & Porter

---

## 一、問題描述

透過 LangBot 整合（Telegram / Discord Bot）發送訊息後，  
Dify Workflow 觸發後持續卡在 **`pending`（等待）** 狀態，無法完成執行，也無法回覆訊息。

### 症狀
- LangBot 日誌顯示任務持續 Polling（輪詢），但工作流從未進入 `running` 或 `succeeded` 狀態
- 使用獨立測試腳本（`test_dify_api.py`）直接呼叫 Dify API，同樣的工作流可以正常執行
- Dify Worker 與 API 服務本身健康，沒有錯誤

---

## 二、根本原因分析

### 原因一：`inputs` 物件缺少 `query` 欄位

Dify 工作流的 `Start` 節點設定了 `query` 作為必填輸入變數。  
LangBot 內建的 `DifyServiceAPIRunner`（位於容器內 `difysvapi.py`）建立 `inputs` 物件時，  
**只包含了 LangBot 自定義的遺留欄位，沒有傳遞 `query`：**

```python
# ❌ 原本錯誤的 inputs（缺少 query）
inputs = {
    'langbot_user_message_text': plain_text,
    'langbot_session_id': query.variables['session_id'],
    'langbot_conversation_id': query.variables['conversation_id'],
    'langbot_msg_create_time': query.variables['msg_create_time'],
    # 👆 Dify 的 Start 節點要求 'query'，但這裡沒有！
}
```

Dify API 收到缺少必填欄位的請求後，工作流無法啟動，持續等待正確輸入 → **Pending 狀態**。

### 原因二：容器內程式碼與宿主機不同步

宿主機的 `difysvapi_current.py` 修改後，  
**並未被 Docker 容器載入**，因為 `docker-compose.yaml` 未設定 bind mount，  
導致容器仍執行映像內的舊版程式碼。

### 原因三：網路連通正常（但排查過程也驗證了這點）

從 `dify-langbot` 容器向 `nginx:80` 發送 GET 請求，回傳 `405 METHOD NOT ALLOWED`，  
這表示**網路是通的**（`405` 代表 nginx 收到了請求，只是方法不對），排除網路故障可能。

---

## 三、解決步驟

### Step 1：修改宿主機程式碼，補上 `query` 欄位

在 `difysvapi_current.py` 的兩個 workflow 方法中，均加入 `'query': plain_text` 的對應：

```python
# ✅ 修正後（同時適用於 _workflow_messages 與 _workflow_messages_chunk）
inputs = {
    'langbot_user_message_text': plain_text,
    'langbot_session_id': query.variables['session_id'],
    'langbot_conversation_id': query.variables['conversation_id'],
    'langbot_msg_create_time': query.variables['msg_create_time'],
    'query': plain_text,  # ✅ Antigravity Fix：對應 Dify Start 節點的 query 欄位
}
```

### Step 2：將修正後的檔案複製進容器

```powershell
# 在 c:\VSCode_Proj\Dify\ 目錄下執行
docker cp difysvapi_current.py dify-langbot:/app/src/langbot/pkg/provider/runners/difysvapi.py
```

### Step 3：重啟容器使修改生效

```powershell
docker restart dify-langbot
```

---

## 四、永久解決方案（建議）

為避免每次重建容器後修改被覆蓋，在 `docker-compose.yaml` 中加入 bind mount：

```yaml
# docker-compose.yaml（langbot 服務段落）
  langbot:
    image: rockchin/langbot:latest
    container_name: dify-langbot
    volumes:
      - ./volumes/langbot/data:/app/data
      # ✅ 加上這行，讓宿主機修改直接套用於容器
      - ../../difysvapi_current.py:/app/src/langbot/pkg/provider/runners/difysvapi.py
    # ...其餘設定不變
```

若日後修改 `difysvapi_current.py`，只需重啟容器即可生效，無需再手動 `docker cp`。

---

## 五、相關檔案一覽

| 檔案路徑 | 說明 |
|---|---|
| `c:\VSCode_Proj\Dify\difysvapi_current.py` | LangBot Dify 整合主程式（宿主機版本） |
| `/app/src/langbot/pkg/provider/runners/difysvapi.py` | 容器內實際運行的整合程式（需與宿主機同步）|
| `/app/src/langbot/libs/dify_service_api/v1/client.py` | Dify API 底層 HTTP 客戶端（含 DEBUG 日誌） |
| `c:\VSCode_Proj\Dify\test_dify_api.py` | 直接呼叫 Dify API 的驗證測試腳本 |
| `c:\VSCode_Proj\Dify\dify\docker\docker-compose.yaml` | Docker 服務編排設定 |

---

## 六、診斷指令速查

```powershell
# 即時查看 LangBot 容器 Log（包含 DEBUG CHUNK 輸出）
docker logs dify-langbot -f --tail 50

# 確認容器內已是修正版本（確認 inputs 包含 query）
docker exec dify-langbot sh -c "grep -n 'query' /app/src/langbot/pkg/provider/runners/difysvapi.py"

# 驗證容器網路能到達 Dify API
docker exec dify-langbot python3 /app/data/diag.py

# 手動同步程式碼並重啟（快速修復用）
docker cp difysvapi_current.py dify-langbot:/app/src/langbot/pkg/provider/runners/difysvapi.py
docker restart dify-langbot
```

---

## 七、重要觀念

> **獨立測試腳本成功 ≠ LangBot 整合正常**  
> 測試腳本自行建構完整的 Payload（含 `query`），所以成功。  
> LangBot 整合依賴 `DifyServiceAPIRunner` 自動組裝 Payload，若缺少欄位則靜默失敗，工作流 Pending。  
>
> 每次懷疑 Pending 問題時，**比對兩者發送的 JSON Payload** 是第一診斷步驟。
