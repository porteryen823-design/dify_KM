# 🚀 Login-App CI/CD 部署手冊

本文件記錄了 `login-app` 的手動本地部署方式（tar + scp）。

**整理人：** Porter  
**更新日期：** 2026-04-23

---

## 🏗️ 基礎環境資訊

| 項目 | 值 |
|------|----|
| **SSH Host Alias** | `dify-aws-gyro` |
| **AWS IP** | `54.250.195.137` |
| **SSH User** | `ubuntu` |
| **PEM Key** | `C:/Users/porte/Downloads/gyro_dify.pem` |
| **SSH Config** | `C:/Users/porte/.ssh/config` |
| **App Port** | `5050` |
| **遠端程式碼路徑** | `~/Dify/login-app/` |
| **資料庫路徑** | `~/Dify/login-app/data/users.db` |
| **容器名稱** | `docker-login_app-1` |

---

## 🚀 手動部署（tar + scp）

> **重要：** 整個 `~/Dify/login-app/` 目錄以 Volume 掛載進容器（`/app`），  
> 因此只需更新檔案後 **restart 容器**即可，**不需要 rebuild image**。

### 完整指令（在本地 Git Bash 執行）

```bash
# Step 1：打包（排除 data/、快取檔案）
tar \
  --exclude='login-app/data' \
  --exclude='login-app/__pycache__' \
  --exclude='login-app/.pytest_cache' \
  --exclude='login-app/*.pyc' \
  -czf /tmp/login-app-deploy.tar.gz login-app/

# Step 2：上傳
scp /tmp/login-app-deploy.tar.gz dify-aws-gyro:/tmp/

# Step 3：遠端解壓 + 重啟容器
ssh dify-aws-gyro "
  tar xzf /tmp/login-app-deploy.tar.gz -C ~/Dify/ &&
  docker restart docker-login_app-1 &&
  docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | grep login
"
```

---

## 📂 核心檔案說明

| 檔案 | 用途 |
|------|------|
| `app.py` | Flask 主程式，所有路由與 DB helpers |
| `Dockerfile` | Python 3.11 環境定義（build 用，volume 模式不需 rebuild） |
| `requirements.txt` | Python 套件清單 |
| `deploy.sh` | 舊版 docker run 部署腳本（目前環境改用 docker compose，保留備用） |
| `templates/` | Jinja2 HTML 模板 |
| `data/` | **不可同步！** 含 `users.db`，僅存在於遠端，由 Docker volume 持久化 |

---

## ⚠️ 重要規範

### 1. data/ 絕對不可覆蓋
* `data/` 目錄內含 `users.db`（所有帳號、App 設定、對話紀錄）
* tar 打包時已明確 `--exclude='login-app/data'`
* 解壓時 tar 只會新增/覆蓋 archive 內的檔案，不會刪除 `data/`

### 2. Volume 掛載架構
遠端容器啟動方式（docker compose）：
```
~/Dify/login-app  →  /app        （程式碼，整個目錄掛載）
~/Dify/login-app/data  →  /app/data  （資料庫，獨立掛載）
```
更新程式碼後只需 `docker restart docker-login_app-1`。

### 3. 安全組設定
* Port `5050` 需在 AWS Console Security Group 開放 TCP 給 `0.0.0.0/0`

---

## 🔍 常用遠端指令

```bash
# 查看容器狀態
ssh dify-aws-gyro "docker ps | grep login"

# 查看即時 log
ssh dify-aws-gyro "docker logs -f docker-login_app-1"

# 進入容器
ssh dify-aws-gyro "docker exec -it docker-login_app-1 bash"

# 確認 data/ 內容
ssh dify-aws-gyro "ls -lh ~/Dify/login-app/data/"
```

---

**建立日期：** 2026-04-23  
**最後修改：** 2026-04-24  
**版本：** v1.1.0  
**整理人：** Antigravity AI & Porter
