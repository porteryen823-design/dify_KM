# Login App 新增計畫

在現有 Dify Docker 環境中，以一個獨立的 **Python Flask** 服務作為統一入口（Portal），提供：
1. **登入驗證**：輸入帳號/密碼，比對本地 JSON 資料表
2. **App List 頁面**：登入後顯示可用的 Dify App 清單，點擊後帶入 `userid`、`username` 導向 Dify App
3. **管理後台**：管理員可新增/刪除/匯入/匯出 User 資料表與 App List 資料表

整個服務透過 Nginx 以 `/portal` 路徑整合，不影響現有 Dify 服務。

---

## User Review Required

> [!IMPORTANT]
> **Port 配置**：Login App 容器內部使用 `5050` port，不對外直接暴露，全程由 Nginx 代理。可在 [.env](file:///c:/VSCode_Proj/Dify/dify/docker/.env) 中設定 `LOGIN_APP_PORT=5050`，建議維持預設值。

> [!IMPORTANT]
> **資料儲存方式**：用戶資料與 App 清單儲存於 `login-app/data/` 目錄的 JSON 檔案（`users.json`, `apps.json`），透過 Docker volume 掛載持久化。**密碼以 SHA-256 Hash 儲存**（非明文）。若您需要改用資料庫（PostgreSQL），請告知，可調整計畫。

> [!IMPORTANT]
> **管理員帳號**：初始管理員帳號為 `admin` / `admin123`（首次啟動後請立即修改）。管理後台網址為 `/portal/admin`，需以管理員身份登入。

> [!WARNING]
> [docker-compose.yaml](file:///c:/VSCode_Proj/Dify/dify/docker/docker-compose.yaml) 標頭標注「Do not modify this file directly」，但此檔案在專案中實際作為運行設定。我們**直接修改**此檔案以加入 `login_app` 服務，並同步更新 [nginx/conf.d/default.conf.template](file:///c:/VSCode_Proj/Dify/dify/docker/nginx/conf.d/default.conf.template)。

---

## Proposed Changes

### Login App 服務本體

#### [NEW] login-app/
新建目錄，存放整個 Login App

#### [NEW] `login-app/Dockerfile`
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5050
CMD ["python", "app.py"]
```

#### [NEW] `login-app/requirements.txt`
```
Flask==3.0.0
flask-session==0.6.0
```

#### [NEW] `login-app/app.py`
Flask 主程式，提供以下路由：
| 路由 | 說明 |
|------|------|
| `GET /portal/` | 重導向至登入頁 |
| `GET /portal/login` | 登入頁 |
| `POST /portal/login` | 登入處理 |
| `GET /portal/apps` | App List 頁（需登入）|
| `GET /portal/logout` | 登出 |
| `GET /portal/admin` | 管理後台首頁（需管理員）|
| `GET/POST /portal/admin/users` | 用戶管理 |
| `GET/POST /portal/admin/apps` | App 管理 |
| `GET /portal/admin/users/export` | 匯出 users.csv |
| `POST /portal/admin/users/import` | 匯入 users.csv |
| `GET /portal/admin/apps/export` | 匯出 apps.csv |
| `POST /portal/admin/apps/import` | 匯入 apps.csv |

#### [NEW] `login-app/data/users.json`
初始範例資料：
```json
[
  {"userid": "admin", "username": "系統管理員", "pwd": "<sha256-hash>", "remark": "管理員", "is_admin": true}
]
```

#### [NEW] `login-app/data/apps.json`
初始範例資料：
```json
[
  {"appname": "客服機器人", "app_address": "http://your-dify-host/chatbot/xxx", "remark": ""}
]
```

#### [NEW] `login-app/templates/` 前端頁面
- `login.html` — 登入頁（深色主題，現代設計）
- `apps.html` — App List（卡片式列表，帶入 userid/username 至 Dify App URL）
- `admin/index.html` — 管理後台
- `admin/users.html` — 用戶管理（表格 + 匯入/匯出）
- `admin/apps.html` — App 管理（表格 + 匯入/匯出）

**導向 Dify App 的方式**：
```
{app_address}?userid={userid}&username={username}
```
（Query String 方式傳遞，Dify App 的對話歡迎語可讀取此參數）

---

### Docker Compose 整合

#### [MODIFY] [docker-compose.yaml](file:///c:/VSCode_Proj/Dify/dify/docker/docker-compose.yaml)

在 `nginx` 服務 **之前** 新增 `login_app` 服務：

```yaml
  # Login Portal App
  login_app:
    build:
      context: ../../login-app
      dockerfile: Dockerfile
    restart: always
    environment:
      SECRET_KEY: ${LOGIN_APP_SECRET_KEY:-login-app-secret-key-change-me}
      APP_PORT: ${LOGIN_APP_PORT:-5050}
    volumes:
      - ../../login-app/data:/app/data
    networks:
      - default
```

---

### Nginx 路由整合

#### [MODIFY] [default.conf.template](file:///c:/VSCode_Proj/Dify/dify/docker/nginx/conf.d/default.conf.template)

在現有 `location /` 之前新增：

```nginx
location /portal {
  proxy_pass http://login_app:5050;
  include proxy.conf;
}
```

---

## Verification Plan

### 手動驗證步驟

1. **啟動服務**：
   ```powershell
   cd c:\VSCode_Proj\Dify\dify\docker
   docker compose --profile weaviate --profile postgresql up -d login_app nginx
   ```

2. **登入測試**：
   - 開啟瀏覽器前往 `http://localhost/portal/login`
   - 輸入 `admin` / `admin123` → 應跳轉至 App List 頁
   - 輸入錯誤密碼 → 應顯示錯誤訊息

3. **App List 測試**：
   - 登入後應看到 App 卡片清單
   - 點擊 App 卡片，應導向 `{app_address}?userid=admin&username=系統管理員`

4. **管理後台 - 用戶管理**：
   - 前往 `http://localhost/portal/admin/users`
   - 新增一位用戶，驗證出現在列表中
   - 點擊「匯出 CSV」，應下載 `users.csv`
   - 上傳合法的 CSV 檔案，應更新用戶列表

5. **管理後台 - App 管理**：
   - 前往 `http://localhost/portal/admin/apps`
   - 新增一個 App，驗證出現在 App List 頁
   - 測試匯入/匯出 CSV

**整理人：** Antigravity AI & Porter
