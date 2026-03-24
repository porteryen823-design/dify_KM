# 使用者應用程式權限管控（Per-User App Access Control）

## 背景說明

目前 `/portal/apps` 顯示的是所有啟用的 App，**所有登入使用者看到的清單完全相同**。功能需求是讓不同帳號看到不同的 App 組合：

- **A123**：可見全部八項 App
- **B123**：可見前幾項 App（例如前四項）
- **C123**：可見部分 App（例如只有一項）

**設計原則：空白 = 沙盒（預設全見）**
> 若某使用者在 `user_app_access` 中**沒有任何設定**，系統仍顯示「所有啟用的 App」（相容舊行為）。
> 一旦替該使用者新增任何一條訪問記錄，系統就切換為**白名單模式**，只顯示明確授權的 App。

---

## 提議變更

### 資料庫層（[app.py](file:///c:/VSCode_Proj/Dify/login-app/app.py)）

#### [MODIFY] [app.py](file:///c:/VSCode_Proj/Dify/login-app/app.py)

1. **新增關聯表** `user_app_access`：
   ```sql
   CREATE TABLE IF NOT EXISTS user_app_access (
       id       INTEGER PRIMARY KEY AUTOINCREMENT,
       userid   TEXT NOT NULL,
       app_id   INTEGER NOT NULL,
       UNIQUE(userid, app_id)
   );
   ```

2. **新增 DB Helper 函數**：
   - `db_get_user_app_ids(userid)` → 取得使用者被授權的 app_id 列表
   - `db_set_user_apps(userid, app_id_list)` → 全量覆寫使用者的授權清單
   - `db_get_apps_for_user(userid)` → 最終使用的查詢：若使用者有授權設定則只回傳授權的 App，否則回傳全部啟用的 App

3. **修改 [apps_list()](file:///c:/VSCode_Proj/Dify/login-app/app.py#515-520) 路由**：呼叫 `db_get_apps_for_user(session['userid'])` 取代 [db_get_all_apps()](file:///c:/VSCode_Proj/Dify/login-app/app.py#224-232)

4. **新增種子資料（測試用）**：
   - A123：授權全部 8 個 App
   - B123：授權前 4 個 App
   - C123：授權第 1 個 App（TSC 機器人）

---

### 後台管理介面

#### [NEW] [admin/user_apps.html](file:///c:/VSCode_Proj/Dify/login-app/templates/admin/user_apps.html)

新增「使用者 App 權限管理」頁面，功能如下：
- 以**使用者選單**選取目標帳號
- 顯示所有啟用中的 App，以 **checkbox** 方式勾選授權
- 提交後全量覆寫該使用者的授權設定

#### [MODIFY] [admin/users.html](file:///c:/VSCode_Proj/Dify/login-app/templates/admin/users.html)

在每位使用者的操作欄加入「**設定 App 權限**」按鈕，點擊跳轉至 `user_apps.html`。

#### [MODIFY] [base.html](file:///c:/VSCode_Proj/Dify/login-app/templates/base.html)

在管理中心下拉選單加入「**使用者 App 權限**」選項。

---

## Verification Plan

### 測試帳號種子

| 帳號 | 可見 App | 模式 |
|------|----------|------|
| A123 | 全部 8 個 | 白名單（全部) |
| B123 | 前 4 個 | 白名單（部分） |
| C123 | 第 1 個（TSC 機器人）| 白名單（一項） |

### 手動驗證步驟

1. 重啟後端（Flask）使 DB 自動遷移並種入測試資料
2. 用 **A123** 登入 → 前往 `/portal/apps` → 確認顯示 8 個 App
3. 用 **B123** 登入 → 前往 `/portal/apps` → 確認只顯示前 4 個 App
4. 用 **C123** 登入 → 前往 `/portal/apps` → 確認只顯示 1 個 App
5. 用管理員帳號登入 → 前往 `/portal/admin` → 確認選單有「使用者 App 權限」
6. 在後台替 C123 額外勾選一個 App 後儲存 → 重新以 C123 登入確認增加

> [!NOTE]
> 若 A123/B123/C123 尚未在 DB 中存在，[init_users_db()](file:///c:/VSCode_Proj/Dify/login-app/app.py#38-171) 會在啟動時自動新增（密碼預設 `1234`）。
