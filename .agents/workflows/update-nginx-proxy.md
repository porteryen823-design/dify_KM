---
description: 自動化更新 Dify Nginx 轉址設定 (ChatID to Portal Path)
---

這個工作流用於當 Dify 應用程式更新（產生新的 Chat ID）時，自動同步更新 Nginx 的反向代理設定與 login-app 的轉址位址。

### 執行步驟

1. **取得輸入資訊**
   - 確定位新的 **Chat ID** (例如: `PFZX7g0ybsvC9c04`)
   - 確定位目標 **入口 Slug** (例如: `/tsc/` 或 `/tsc_app/`)

2. **更新 login-app 配置**
   - 讀取 `c:\VSCode_Proj\Dify\login-app\data\apps.json`
   - 找到對應的 `slug` 項目
   - 將 `app_address` 更新為 `http://localhost:8080/chat/[ChatID]`

3. **更新 Nginx 設定檔 (如果有特定路徑需求)**
   - 檢查 Dify Docker 目錄下的 Nginx 配置 (通常在 `c:\VSCode_Proj\Dify\dify\docker\nginx\conf.d\default.conf`)
   - 搜尋對應的 `location` 區塊
   - 更新 `proxy_pass` 或 `rewrite` 規則，確保對應至新的 Chat ID 路徑

4. **驗證 Nginx 配置並重啟**
// turbo
   - 進入 docker 目錄執行：
     `docker-compose -p dify exec nginx nginx -t`
// turbo
   - 如果測試通過，執行重載：
     `docker-compose -p dify exec nginx nginx -s reload`

5. **最終確認**
   - 測試 `/portal/goto/[slug]` 是否能成功跳轉並正確帶入 `user` 與 `username` 參數。

---
**整理人：** Antigravity AI & Porter
