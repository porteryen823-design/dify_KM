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
# 請務必提供欲還原的備份資料夾絕對路徑
powershell -ExecutionPolicy Bypass -File C:\VSCode_Proj\Dify\scripts\restore-dify.ps1 -TargetFolder "C:\VSCode_Proj\Dify\backups\YYYYMMDD_HHMMSS"
```

### 🛡️ 還原安全機制 (內建流程)
1. **自動快照**：腳本會先自動執行一次完整備份，保存當前毀損或不想要的狀態（以防還原後後悔）。
2. **互動確認**：腳本會顯示目標路徑並要求使用者輸入 `Y` 才會開始覆寫。
3. **全自動部署**：腳本會依序還原 `.env` → `PostgreSQL` → `Weaviate` → `Storage` → `Redis`。
4. **服務重啟**：還原完成後，腳本會自動重啟所有 Dify 服務以套用設定。

---

---

## ⚠️ 注意事項
1. **自動清理**：腳本預設保留 **7 天**備份，舊檔案自動刪除，重要備份請移至異地。
2. **Weaviate 鎖定**：Weaviate `.db` 檔案在容器運行時被鎖定，腳本採用 `docker exec tar + docker cp` 策略繞過 Windows 鎖定限制。
3. **安全性**：備份目錄含有 API Keys（`.env` 檔案），請妥善保管並設定存取權限。
4. **完整還原順序**：建議按 PostgreSQL → .env → Storage → Weaviate → Redis 的順序還原，最後再重啟服務。
