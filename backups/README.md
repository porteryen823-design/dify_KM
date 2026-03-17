# Dify 系統完整備份說明文件 (Windows PowerShell 版)

> **整理人：** Antigravity AI & Porter
> **最後更新：** 2026-03-17

本目錄存放 Dify 系統自動化備份檔案，涵蓋 Dify 五大備份範圍。

---

## 📊 備份完整性狀態

| # | 備份項目 | 狀態 | 說明 |
| :---: | :--- | :---: | :--- |
| 1 | **PostgreSQL** (`docker-db_postgres-1`) | ✅ 已備份 | 核心資料（帳號、應用、Prompt、知識庫 metadata） |
| 2 | **Weaviate 向量庫** (`docker-weaviate-1`) | ✅ 已備份 | 知識庫分段向量索引 |
| 3 | **Storage 原始檔案** (`/volumes/app/storage`) | ✅ 已備份 | 知識庫上傳文件、對話附件 |
| 4 | **Redis** (`docker-redis-1`) | ✅ 已備份 | 快取與任務佇列狀態（選配） |
| 5 | **.env 環境變數** (`/docker/.env`) | ✅ 已備份 | API 金鑰、模型設定 |

---

## 📁 備份檔案說明

| 檔案格式 | 內容 | 大小參考 |
| :--- | :--- | :--- |
| `dify_postgres_YYYYMMDD_HHMMSS.zip` | PostgreSQL 邏輯 Dump 壓縮檔 | ~48 MB |
| `dify_weaviate_YYYYMMDD_HHMMSS.zip` | Weaviate 向量庫完整快照 | ~22 MB |
| `dify_storage_YYYYMMDD_HHMMSS.zip` | 原始文件儲存（知識庫上傳） | ~16 MB |
| `dify_redis_YYYYMMDD_HHMMSS.rdb` | Redis 資料快照 | ~1 MB |
| `dify_env_YYYYMMDD_HHMMSS.env` | 環境變數設定檔 | < 1 KB |
| `backup_log.txt` | 備份執行詳情與錯誤日誌 | — |

---

## 🚀 執行備份

**腳本路徑：** `C:\VSCode_Proj\Dify\scripts\backup-dify.ps1`

### 手動執行
```powershell
powershell -ExecutionPolicy Bypass -File C:\VSCode_Proj\Dify\scripts\backup-dify.ps1
```

### 設定自動排程（Windows 工作排程器）
1. 開啟「工作排程器 (Task Scheduler)」
2. 建立基本工作，設定觸發時間（建議每日凌晨）
3. 動作選擇「啟動程式」，填入：
   - **程式：** `powershell.exe`
   - **引數：** `-ExecutionPolicy Bypass -File C:\VSCode_Proj\Dify\scripts\backup-dify.ps1`

---

## 🛠 還原指南 (Restore Guide)

我們提供了全自動化的還原腳本，內建 **「還原前強制安全性備份」** 機制，確保您的資料萬無一失。

### 使用自動化還原腳本
**腳本路徑：** `C:\VSCode_Proj\Dify\scripts\restore-dify.ps1`

**執行指令：**
```powershell
# 1. 安全還原 (會要求輸入 Y 確認)
powershell -ExecutionPolicy Bypass -File C:\VSCode_Proj\Dify\scripts\restore-dify.ps1 -TargetFolder "C:\VSCode_Proj\Dify\backups\YYYYMMDD_HHMMSS"

# 2. 強制還原 (自動化/壓力測試用，跳過確認)
powershell -ExecutionPolicy Bypass -File C:\VSCode_Proj\Dify\scripts\restore-dify.ps1 -TargetFolder "C:\VSCode_Proj\Dify\backups\YYYYMMDD_HHMMSS" -Force
```

### 🛡️ 專業化安全機制 (內建流程)
1. **安全性強制備份**：腳本會先自動執行一次完整備份。若備份腳本回傳失敗（如空間不足），還原將**立即中止**以保護現場。
2. **PostgreSQL 就緒監控**：還原過程中，腳本會自動偵測資料庫容器狀態，確保連線就緒後才進行 `DROP SCHEMA` 與資料導入。
3. **Weaviate 內部解壓縮**：針對 Windows 檔案鎖定問題，腳本切換至「容器內解壓」模式，保證向量索引精準還原。
4. **互動/自動雙模式**：支援手動輸入 `Y` 確認，或透過 `-Force` 開關進行無人值守遷移。
5. **服務全自動部署**：依序還原 `.env` → `Postgres` → `Weaviate` → `Storage` → `Redis`。

---

## ⚠️ 注意事項與故障排除
1. **自動清理**：腳本執行完畢後會自動清理 `temp` 空間；每日備份預設保留 **7 天**。
2. **路徑限制**：目前腳本採用絕對路徑。若遷移至新電腦，請確保目錄結構一致，或修改腳本變數。
3. **安全性**：`.env` 備份含敏感金鑰，建議備份目錄設定嚴格存取權限。
4. **還原卡住處理**：若還原期間顯示 `Waiting for PostgreSQL to be ready` 超過 60 秒，請檢查 `docker logs docker-db_postgres-1` 確認資料庫啟動狀況。
5. **GitIgnore**：`.gitignore` 已設定忽略實際備份檔與日誌，僅上傳腳本與本 README 文件。
