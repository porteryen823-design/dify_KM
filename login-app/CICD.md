# 🚀 Login-App CI/CD 部署手冊

本文件記錄了 `login-app` 的兩種部署方式：**GitHub Actions (自動)** 與 **Local Direct (手動/本地)**。

**整理人：** Antigravity AI & Porter  
**更新日期：** 2026-03-24

---

## 🏗️ 基礎環境資訊
* **AWS IP:** `52.196.249.194`
* **SSH User:** `ubuntu`
* **PEM Key Path:** `C:\Users\porte\Downloads\dify_ubuntu2.pem`
* **App Port:** `5050`
* **遠端路徑:** `~/apps/login-app`

---

## 🛠️ 方式 A：GitHub Actions (全自動部署)
適用於團隊協作或正式環境更新。當你 `git push` 到 GitHub 時，AWS 會自動更新。

### 1. 設定 GitHub Secrets
前往 GitHub 倉庫的 **Settings > Secrets and variables > Actions**，新增以下 Secrets：

| Secret 名稱 | 內容範例 |
|-------------|----------|
| `EC2_HOST` | `52.196.249.194` |
| `EC2_USER` | `ubuntu` |
| `EC2_PORT` | `22` |
| `EC2_KEY` | `dify_ubuntu2.pem` 的完整文字內容 |

### 2. 工作流檔案 (Workflow)
存放於 [`.github/workflows/deploy.yml`](file:///c:/VSCode_Proj/Dify/.github/workflows/deploy.yml)。  
**觸發條件：** 全自動，異動 `login-app/` 並 Push 後自動啟動。

---

## 💻 方式 B：本地直接部署 (Local Direct)
適用於快速測試或不經過 GitHub 的情況。

### 1. 使用 PowerShell 一鍵部署
直接在 VSCode 或 PowerShell 執行：
```powershell
.\login-app\deploy-local-ps.ps1
```

### 2. 使用 Antigravity 工作流指令
在對話框輸入：
```
/deploy-aws-local
```

---

## 📂 核心檔案說明

| 檔案名稱 | 用途 |
|----------|------|
| [`login-app/deploy.sh`](file:///c:/VSCode_Proj/Dify/login-app/deploy.sh) | **最重要！** 這是 AWS 端執行的腳本。負責 Build 容器、重啟服務。 |
| [`login-app/Dockerfile`](file:///c:/VSCode_Proj/Dify/login-app/Dockerfile) | 定義 Python 3.11 環境與啟動指令。 |
| [`login-app/deploy-local-ps.ps1`](file:///c:/VSCode_Proj/Dify/login-app/deploy-local-ps.ps1) | 本地端專用的連線與同步腳本。 |

---

## ⚠️ 重要規範與注意事項

### 1. 資料庫持久化 (Persistence)
* **規則：** 本地部署與 GitHub Actions 均已排除 `data/` 目錄的同步。
* **原因：** 確保 AWS 上 `data/` 裡的 `users.db` 或 CSV 檔案**不會**被本地空白資料覆蓋。
* **路徑映射：** Docker 啟動時使用 `-v ~/apps/login-app/data:/app/data`。

### 2. 安全組設定 (Security Groups)
* 如果無法訪問網頁，請確認 AWS Console 開放了 **Port 5050 (TCP)** 給 `0.0.0.0/0`。

### 3. 如何修正部署邏輯？
* 若要修改部署方式（如更換 Port），請優先修改 [`login-app/deploy.sh`](file:///c:/VSCode_Proj/Dify/login-app/deploy.sh)。

---
**整理人：** Antigravity AI & Porter
