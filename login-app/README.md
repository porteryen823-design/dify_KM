# Login-App — QA Bot Portal v1.0.3

**版本：v1.0.3**　｜　**整理人：Porter & Antigravity AI**　｜　**更新日期：2026-04-24**

Dify 前台登入入口，提供帳號驗證、App 權限管理、內嵌聊天介面，以及對外開放的使用者查詢 API。

---

## 目錄

- [架構概覽](#架構概覽)
- [目錄結構](#目錄結構)
- [資料庫結構](#資料庫結構)
- [登入邏輯](#登入邏輯)
- [功能說明](#功能說明)
- [路由一覽](#路由一覽)
- [環境變數](#環境變數)
- [部署方式](#部署方式)
- [版本紀錄](#版本紀錄)

---

## 架構概覽

```
使用者瀏覽器
    │
    ▼
Flask (port 5050)  ──► SQLite (data/users.db)
    │
    ▼
Dify API (http://api:5001)
```

- **語言**：Python 3.11 / Flask 3.0
- **資料庫**：SQLite（`data/users.db`），啟動時自動建立與 migration
- **容器**：Docker，映像定義於 `Dockerfile`
- **Dify 溝通**：Flask 作為 proxy，避免前端直接暴露 API Key

---

## 目錄結構

```
login-app/
├── app.py                  # 主程式，所有路由與 DB helpers
├── Dockerfile
├── requirements.txt
├── deploy.sh               # AWS 端部署腳本
├── update_db_test_data.py  # 手動更新測試資料用
├── data/
│   ├── users.db            # SQLite 主資料庫（掛載持久化）
│   ├── users.json          # 舊版資料（migration 來源，已棄用）
│   └── apps.json           # 舊版資料（migration 來源，已棄用）
└── templates/
    ├── base.html
    ├── login.html
    ├── apps.html           # App 清單頁
    ├── chat.html           # 內嵌聊天頁
    └── admin/
        ├── index.html
        ├── users.html
        ├── apps.html
        ├── user_apps.html  # 使用者 App 權限設定
        └── token_log.html
```

---

## 資料庫結構

### `users`
| 欄位 | 說明 |
|------|------|
| `userid` (PK) | 帳號（如 A123 或 email） |
| `username` | 顯示名稱 |
| `pwd` | SHA-256 密碼雜湊 |
| `phone` / `ext` / `email` / `wechat` | 聯絡資訊 |
| `is_admin` | 是否為管理員 |
| `is_active` | 是否啟用 |

### `apps`
| 欄位 | 說明 |
|------|------|
| `id` (PK) | 自動遞增 |
| `slug` | 唯一代碼（如 `tsc_app`） |
| `appname` | 顯示名稱 |
| `app_address` | Dify 聊天 URL |
| `api_key` | 對應 Dify App 的 API Key |
| `use_token` | 是否啟用 Token 閘道模式 |
| `sort_order` | 排列順序 |
| `is_active` | 是否顯示 |

### `user_app_access`
白名單模式：記錄哪位 user 有哪些 app 的存取權。無記錄時視為沙盒（全開放）。

### `token_log`
每次使用者透過閘道跳轉時，記錄 UUID token → userid 的對應，供 Dify HTTP Node 查詢身分。

### `user_conversations` *(v1.0.2 新增)*
| 欄位 | 說明 |
|------|------|
| `userid` | 使用者帳號 |
| `app_slug` | App 代碼（如 `tsc_app`） |
| `conversation_id` | Dify 回傳的對話 ID |
| `updated_at` | 最後更新時間 |

**複合主鍵 (userid, app_slug)**，確保每位使用者對每個 App 只有一筆對話記錄，跨裝置、重新登入後仍繼續同一對話。

### `message_feedback`
記錄使用者對 AI 回覆的按讚/倒讚與具體不滿意原因（因 Dify 歷史 API 不回傳原因，故採本地儲存補強）。
| 欄位 | 說明 |
|------|------|
| `message_id` (PK) | 關聯至 Dify 的對話訊息 ID |
| `rating` | 評分結果（`like` 或 `dislike`） |
| `content` | 使用者填寫的不滿意原因 |
| `created_at` | 紀錄建立時間 |

---

## 登入邏輯

### 1. Email 網域登入（免密碼）
- 輸入 `@gyro.com.tw` 或 `@gyrobot.com` 的 Email 即可登入
- 不需填密碼、不查資料庫
- 自動繼承 **A123** 的 App 權限範本

### 2. 帳號密碼登入
- 查詢 `users` 資料表，比對 SHA-256 雜湊密碼
- 帳號需為 `is_active=1`

### 3. 預設測試帳號（密碼均為 `1234`）
| 帳號 | 說明 | 權限 |
|------|------|------|
| `A123` | UserA | 全部 App |
| `B123` | UserB | 前 4 個 App |
| `C123` | UserC | 單一 App |
| `admin` | 管理員 | 後台全部功能 |

---

## 功能說明

### 聊天介面（`/portal/embedded_chat`）
- 內嵌在 Portal 頁面，不直接開啟 Dify 網址
- Flask 作為 proxy（`/portal/chat/send`）轉送訊息至 Dify，自動帶入 `user=userid`
- 支援 Streaming 回應解析（`message` / `text_chunk` / `workflow_finished` 事件）
- 自動過濾 `<think>...</think>` 標籤（DeepSeek 等推理模型）

### 對話持久化（v1.0.2）
- `conversation_id` 存入 `user_conversations` DB，與 userid 綁定
- 每次登入、換裝置，皆自動接續同一對話
- Dify 日誌的「使用者或賬戶」欄位保持一致，不會重複產生新帳戶

### 歷史對話載入（v1.0.2）
- 聊天頁 Topbar 新增「歷史紀錄」按鈕
- 點擊後呼叫 `/portal/chat/history`，Proxy 至 Dify `/v1/messages`
- 以分隔線標示歷史訊息，視覺上區隔新對話
- 第二次點擊直接捲到頁面頂部，不重複呼叫 API

### 訊息回饋（like / dislike）
- 每則 Bot 回應下方有「有幫助 / 無幫助」按鈕
- 點「無幫助」會展開原因輸入框，送出後記錄至 Dify

### App 白名單權限
- 管理員可在 `/portal/admin/user_apps` 設定每位使用者可存取哪些 App
- 未設定任何規則 → 沙盒模式（顯示全部 is_active App）
- Email 網域使用者自動套用 A123 的權限範本

### Token 閘道
- `use_token=1` 的 App 進入時，會產生 UUID token 並記錄至 `token_log`
- Dify HTTP Node 可呼叫 `/portal/verify_token?token=<uuid>` 查詢身分
- 亦支援 `/portal/verify_token?user=<userid>` 直查模式

### 對外 API（供 Dify 工具呼叫）
| 端點 | 方法 | 說明 |
|------|------|------|
| `/api/v1/user-query` | GET | 模糊搜尋使用者聯絡資訊（q / userid / wechat） |
| `/api/v1/sql-query` | POST | 限 SELECT 語句的 SQL 查詢，僅限 users 資料表 |

兩者均支援 `SYSTEM_API_KEY` 環境變數進行 Bearer Token 驗證。

### 管理後台（`/portal/admin/*`）
| 路徑 | 功能 |
|------|------|
| `/admin/users` | 新增 / 編輯 / 刪除 / 重設密碼 / CSV 匯出入 |
| `/admin/apps` | 新增 / 編輯 / 刪除 App，設定 API Key |
| `/admin/user_apps` | 設定使用者 App 存取白名單 |
| `/admin/token_log` | 查看跳轉 token 紀錄 |
| `/admin/chat_history` | 查詢全站問答歷史紀錄與 CSV 匯出 |

---

## 路由一覽

### 公開路由
| 路徑 | 說明 |
|------|------|
| `GET /portal/login` | 登入頁 |
| `POST /portal/login` | 登入處理 |
| `GET /portal/logout` | 登出 |

### 使用者路由（需登入）
| 路徑 | 說明 |
|------|------|
| `GET /portal/apps` | App 清單 |
| `GET /portal/embedded_chat` | 內嵌聊天頁 |
| `POST /portal/chat/send` | 發送訊息（Dify proxy） |
| `GET /portal/chat/history` | 載入歷史對話 |
| `POST /portal/chat/feedback` | 送出訊息評分 |
| `GET /portal/goto/tsc_app` | TSC App 閘道入口 |
| `GET /portal/go/<slug>` | 通用 Slug 入口 |

### 驗證 API
| 路徑 | 說明 |
|------|------|
| `GET /portal/verify_token` | Token / userid 身分驗證 |

---

## 環境變數

| 變數名稱 | 預設值 | 說明 |
|----------|--------|------|
| `SECRET_KEY` | `default-dev-secret-key-1234` | Flask Session 加密金鑰，**正式環境務必修改** |
| `APP_VERSION` | `v1.0.3` | 顯示於頁面的版本號 |
| `SYSTEM_API_KEY` | 無 | 啟用後，對外 API 需帶 Bearer Token |

---

## 部署方式

詳見 [CICD.md](CICD.md)。

**快速摘要：**
- **自動部署**：Push 至 GitHub `login-app/` 路徑 → GitHub Actions 自動部署至 AWS EC2
- **手動部署**：`.\login-app\deploy-local-ps.ps1`
- **資料持久化**：Docker 啟動時掛載 `-v ~/apps/login-app/data:/app/data`，`data/` 目錄不隨部署覆蓋

---

## 版本紀錄

### v1.0.3 (2026-04-24)
- 實作「問答歷史查詢」後台介面 (`/admin/chat_history`)
- 透過 API 自動合併 Dify PostgreSQL (問答紀錄) 與本地 SQLite (回饋評分) 資料
- 支援依時間區間、特定 App、評分狀態 (Like/Dislike) 進行資料過濾篩選
- **Markdown 渲染**：後台 AI 回答支援 Markdown 格式（表格、清單）美觀顯示
- 提供查詢結果完整匯出 CSV (UTF-8 BOM)，方便後續樞紐分析

### v1.0.2 (2026-04-23)
- 新增 `user_conversations` 資料表，持久化 Dify `conversation_id`
- 每位使用者登入後自動接續同一對話，Dify 日誌不再產生重複帳戶
- 新增 `GET /portal/chat/history` 路由，代理 Dify 歷史訊息 API
- 聊天頁 Topbar 新增「歷史紀錄」按鈕

### v1.0.1 (2026-03-24)
- 初始版本發佈
- 帳號密碼 + Email 網域雙模式登入
- App 白名單權限管理
- 內嵌 Dify 聊天介面（Streaming）
- 訊息 like / dislike 回饋功能
- Token 閘道與身分驗證 API
- 管理後台（users / apps / user_apps / token_log）
- CSV 匯出入功能
