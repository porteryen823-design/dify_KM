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

### 原因四：API 超時 (ReadTimeout) 或外部 IP 迴圈 (Hairpin) 問題

儘管 URL 格式正確，但如果 LangBot 的 Base URL 設為外部 Public IP（如 `http://52.196.249.194/v1`），會導致容器必須繞行公網/AWS VPC 外網再回到同機的 Nginx，這可能引發：
1. **TCP 封包丟失 / 網路延遲**
2. 預設的 **`httpx` timeout=30.0 秒**過短，無法等待 LLM 產生回應而拋出 `httpx.ReadTimeout`。

### 原因五：Dify App 必填參數缺失 (`output_language`)

某些 Dify App（如「桃花源問答 V1.0」）在 `Start` 節點或全域設定中將 `output_language` 設為必填。
LangBot 在建構 `inputs` 時預設並不會包含此欄位，導致 Dify 回傳 `400 Bad Request: output_language is required`。

當這些例外發生且未被妥善捕捉並回傳 UI 時，任務會卡在 **Pending**。

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

### Step 4：最佳化連線位址與超時設定 (解決 ReadTimeout)

在 Dify-LangBot 的 Web UI 中配置 **Dify Service API** 整合時：
- **❌ 避免使用公網 IP**：`http://52.196.249.194/v1`
- **✅ 改用內部 Docker 名稱**：應設為 `http://nginx/v1`（基於 docker-compose 同網段的自動域名解析）

這大舉提升穩定度，並確保不受外部防火牆或 NAT Hairpin 阻擾。
此外，遠端容器的 `client.py` 預設 30 秒有可能因生成速度太慢而斷開，建議透過腳本或 `sed` 將其提昇為 300 秒。

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

若日後修改 `difysvapi_current.py` 或修正 `client.py`，只需重啟容器即可生效，無需再手動 `docker cp`。

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

---

## 八、2026-04-09 補充：補入 `output_language` 修復

若 Dify App 要求 `output_language` 必填，可透過以下 Python 腳本在容器內進行熱修復：

```python
import os
file_path = '/app/src/langbot/pkg/provider/runners/difysvapi.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()
new_content = content.replace('inputs = {}', "inputs = {'output_language': '繁體中文'}")
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)
```

修改後執行 `docker restart dify-langbot`。
