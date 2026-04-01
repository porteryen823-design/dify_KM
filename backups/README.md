# Dify 系統完整備份說明文件 (Windows PowerShell 版)

> **整理人：** Antigravity AI & Porter
> **最後更新：** 2026-03-31

本目錄存放 Dify 系統自動化備份檔案，區分 **本地 (local)** 與 **AWS 生產環境 (dify-aws-gyro)** 兩套。

---

## 📁 目錄結構

```
backups/
├── local/                          # 本地 Docker Dify 備份
│   ├── 20260317_103240/            # 每次備份獨立子目錄（timestamp）
│   │   ├── dify_postgres_*.zip
│   │   ├── dify_weaviate_*.zip
│   │   ├── dify_storage_*.zip
│   │   ├── dify_redis_*.rdb
│   │   └── dify_env_*.env
│   └── backup_log.txt
│
├── dify-aws-gyro/                  # AWS EC2 Gyro 環境備份（透過 SSH 拉取）
│   ├── 20260331_101000/
│   │   ├── dify_postgres_*.zip
│   │   ├── dify_weaviate_*.zip
│   │   ├── dify_storage_*.zip
│   │   ├── dify_redis_*.rdb
│   │   └── dify_env_*.env
│   └── backup_log.txt
│
└── README.md                       # 本說明文件
```

---

## 📊 備份完整性狀態

| # | 備份項目 | 狀態 | 說明 |
| :---: | :--- | :---: | :--- |
| 1 | **PostgreSQL** | ✅ 已備份 | 核心資料（帳號、應用、Prompt、知識庫 metadata） |
| 2 | **Weaviate 向量庫** | ✅ 已備份 | 知識庫分段向量索引 |
| 3 | **Storage 原始檔案** | ✅ 已備份 | 知識庫上傳文件、對話附件 |
| 4 | **Redis** | ✅ 已備份 | 快取與任務佇列狀態（選配） |
| 5 | **.env 環境變數** | ✅ 已備份 | API 金鑰、模型設定 |

---

## 📋 備份檔案格式

| 檔案格式 | 內容 | 大小參考 |
| :--- | :--- | :--- |
| `dify_postgres_YYYYMMDD_HHMMSS.zip` | PostgreSQL 邏輯 Dump 壓縮檔 | ~48 MB |
| `dify_weaviate_YYYYMMDD_HHMMSS.zip` | Weaviate 向量庫完整快照 | ~22 MB |
| `dify_storage_YYYYMMDD_HHMMSS.zip` | 原始文件儲存（知識庫上傳） | ~16 MB |
| `dify_redis_YYYYMMDD_HHMMSS.rdb` | Redis 資料快照 | ~1 MB |
| `dify_env_YYYYMMDD_HHMMSS.env` | 環境變數設定檔 | < 1 KB |

---

## 🚀 執行備份

### 環境一：本地 Docker (local)

**腳本路徑：** `C:\VSCode_Proj\Dify\scripts\backup-dify-local.ps1`

```powershell
powershell -ExecutionPolicy Bypass -File C:\VSCode_Proj\Dify\scripts\backup-dify-local.ps1
```

- 備份輸出：`backups\local\<timestamp>\`
- 保留天數：**7 天**
- 容器來源：本機 Docker (`docker-db_postgres-1` 等)

---

### 環境二：AWS EC2 Gyro (dify-aws-gyro)

**腳本路徑：** `C:\VSCode_Proj\Dify\scripts\backup-dify-aws-gyro.ps1`

```powershell
powershell -ExecutionPolicy Bypass -File C:\VSCode_Proj\Dify\scripts\backup-dify-aws-gyro.ps1
```

- 備份輸出：`backups\dify-aws-gyro\<timestamp>\`
- 保留天數：**14 天**（AWS 生產環境保留更長）
- 連線方式：SSH Host `dify-aws-gyro`（需設定 `~/.ssh/config`）
- 傳輸方式：在遠端容器執行備份 → SCP 拉取至本地

#### SSH Config 需求 (`~/.ssh/config`)
```
Host dify-aws-gyro
    HostName <EC2 Public IP 或 DNS>
    User ec2-user
    IdentityFile ~/.ssh/<your-key>.pem
```

---

## 🛠 還原指南 (Restore Guide)

> [!CAUTION]
> 還原會覆蓋目標環境的所有資料。腳本內建「還原前強制安全性備份」機制，請確保有足夠磁碟空間。

### 環境一：本地 Docker (local)

**腳本路徑：** `C:\VSCode_Proj\Dify\scripts\restore-dify-local.ps1`

```powershell
# 安全還原（會詢問 Y/N 確認）
powershell -ExecutionPolicy Bypass -File C:\VSCode_Proj\Dify\scripts\restore-dify-local.ps1 `
  -TargetFolder "C:\VSCode_Proj\Dify\backups\local\YYYYMMDD_HHMMSS"

# 強制還原（跳過確認，適合自動化流程）
powershell -ExecutionPolicy Bypass -File C:\VSCode_Proj\Dify\scripts\restore-dify-local.ps1 `
  -TargetFolder "C:\VSCode_Proj\Dify\backups\local\YYYYMMDD_HHMMSS" -Force
```

**內建流程：**
1. 自動執行本地安全備份（失敗即中止）
2. 互動確認（或 `-Force` 跳過）
3. 依序還原 `.env` → PostgreSQL → Weaviate → Storage → Redis
4. 自動重啟本地 Docker Compose 服務

---

### 環境二：AWS EC2 Gyro (dify-aws-gyro)

**腳本路徑：** `C:\VSCode_Proj\Dify\scripts\restore-dify-aws-gyro.ps1`

```powershell
# 安全還原（會詢問 Y/N 確認）
powershell -ExecutionPolicy Bypass -File C:\VSCode_Proj\Dify\scripts\restore-dify-aws-gyro.ps1 `
  -TargetFolder "C:\VSCode_Proj\Dify\backups\dify-aws-gyro\YYYYMMDD_HHMMSS"

# 強制還原（跳過確認）
powershell -ExecutionPolicy Bypass -File C:\VSCode_Proj\Dify\scripts\restore-dify-aws-gyro.ps1 `
  -TargetFolder "C:\VSCode_Proj\Dify\backups\dify-aws-gyro\YYYYMMDD_HHMMSS" -Force
```

**內建流程：**
1. 測試 SSH 連線至 `dify-aws-gyro`
2. 自動執行遠端安全備份（先快照現況，失敗即中止）
3. 互動確認（或 `-Force` 跳過）
4. 透過 SCP 將備份檔上傳至 EC2 `/tmp/dify_restore_gyro/`
5. 透過 SSH 在 EC2 容器內執行還原（.env → PostgreSQL → Weaviate → Storage → Redis）
6. 自動重啟 EC2 Dify Docker Compose 服務
7. 清除 EC2 上的暫存檔

---

## 🔧 設定自動排程（Windows 工作排程器）

建議各環境設定獨立的排程工作：

| 環境 | 腳本 | 建議頻率 |
| :--- | :--- | :--- |
| local | `backup-dify-local.ps1` | 每日 02:00 |
| dify-aws-gyro | `backup-dify-aws-gyro.ps1` | 每日 03:00 |

設定步驟：
1. 開啟「工作排程器 (Task Scheduler)」
2. 建立基本工作，設定觸發時間
3. 動作選擇「啟動程式」：
   - **程式：** `powershell.exe`
   - **引數：** `-ExecutionPolicy Bypass -File C:\VSCode_Proj\Dify\scripts\backup-dify-local.ps1`

---

## ⚠️ 注意事項與故障排除

1. **AWS 備份前提**：本機需能以 `ssh dify-aws-gyro` 免密碼連線 EC2。
2. **自動清理**：local 保留 7 天，dify-aws-gyro 保留 14 天。
3. **路徑限制**：腳本採用絕對路徑，遷移電腦時需調整腳本變數。
4. **安全性**：`.env` 備份含敏感金鑰，建議備份目錄設定嚴格存取權限。
5. **Weaviate 警告**：若 Weaviate 備份過小（< 1MB）會記錄 Warning 但不中止其他項目備份。
6. **GitIgnore**：`.gitignore` 已設定忽略實際備份檔與日誌，僅上傳腳本與本 README 文件。
