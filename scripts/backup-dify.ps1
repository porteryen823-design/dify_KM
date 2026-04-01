# Dify Full Backup Script (Windows PowerShell) - LOCAL Environment
# Covers: PostgreSQL, Weaviate, Redis, Storage Files, .env
# Creator: Antigravity AI & Porter
#
# [NOTICE] 此腳本已更新為輸出至 backups\local\ 子目錄。
# 建議改用新腳本: backup-dify-local.ps1 (功能相同，命名更清楚)
# AWS Gyro 環境請改用: backup-dify-aws-gyro.ps1

$BackupDir = "C:\VSCode_Proj\Dify\backups\local"
$Date = Get-Date -Format "yyyyMMdd_HHmmss"
$LogFile = "$BackupDir\backup_log.txt"
$RetentionDays = 7

# Dify Source Paths (Bind Mounts - confirmed via docker inspect)
$DifyDockerRoot = "C:\VSCode_Proj\Dify\dify\docker"
$VolumePgData    = "$DifyDockerRoot\volumes\db\data"
$VolumeWeaviate  = "$DifyDockerRoot\volumes\weaviate"
$VolumeRedis     = "$DifyDockerRoot\volumes\redis\data"
$VolumeStorage   = "$DifyDockerRoot\volumes\app\storage"
$EnvFile         = "$DifyDockerRoot\.env"

# Container names (confirmed via docker ps)
$DbContainer    = "docker-db_postgres-1"
$RedisContainer = "docker-redis-1"
$DbUser = "postgres"
$DbName = "dify"

# Ensure backup root directory exists
if (!(Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir | Out-Null
}

# Create a sub-directory for this specific backup run
$CurrentBackupFolder = Join-Path $BackupDir $Date
New-Item -ItemType Directory -Path $CurrentBackupFolder | Out-Null

function Write-Log {
    param([string]$Message)
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $FormattedMessage = "[$Timestamp] $Message"
    Write-Host $FormattedMessage
    $FormattedMessage | Out-File -FilePath $LogFile -Append -Encoding utf8
}

Write-Log "====== Dify Full Backup Start ======"

# Check DB container is running
$RunningContainers = docker ps --format "{{.Names}}"
if ($DbContainer -notin $RunningContainers) {
    Write-Log "Error: DB Container $DbContainer is not running. Aborting."
    exit 1
}

# ───────────────────────────────────────────────────────
# 1. PostgreSQL Backup (pg_dump - consistent logical dump)
# ───────────────────────────────────────────────────────
Write-Log "[1/5] Backing up PostgreSQL ($DbContainer)..."
$TempSqlFile  = "/tmp/dify_$Date.sql"
$LocalSqlFile = Join-Path $CurrentBackupFolder "dify_$Date.sql"
$PgZipFile    = Join-Path $CurrentBackupFolder "dify_postgres_$Date.zip"

try {
    docker exec $DbContainer pg_dump -U $DbUser -d $DbName -f $TempSqlFile
    docker cp "${DbContainer}:${TempSqlFile}" $LocalSqlFile
    docker exec $DbContainer rm $TempSqlFile
    
    # 檢查內容是否有效 (SQL 預期至少 10KB)
    if ((Get-Item $LocalSqlFile).Length -lt 10KB) { throw "PostgreSQL dump file is too small." }
    
    Compress-Archive -Path $LocalSqlFile -DestinationPath $PgZipFile -Force
    Remove-Item $LocalSqlFile
    Write-Log "    PostgreSQL backup OK: $PgZipFile"
} catch {
    Write-Log "Error: PostgreSQL backup failed! $_"
    exit 1
}

# ───────────────────────────────────────────────────────
# 2. Weaviate Vector Store Backup (direct volume copy)
# ───────────────────────────────────────────────────────
Write-Log "[2/5] Backing up Weaviate vector store..."
$WeaviateZip = Join-Path $CurrentBackupFolder "dify_weaviate_$Date.zip"

try {
    # Use docker cp + tar inside container to avoid Windows file lock on .db files
    $WeaviateTar = "/tmp/weaviate_backup_$Date.tar.gz"
    docker exec docker-weaviate-1 sh -c "tar -czf $WeaviateTar /var/lib/weaviate 2>/dev/null"
    docker cp "docker-weaviate-1:$WeaviateTar" $WeaviateZip
    docker exec docker-weaviate-1 rm $WeaviateTar
    
    # 檢查 Weaviate 備份 (預期至少 1MB)
    if ((Get-Item $WeaviateZip).Length -lt 1MB) { throw "Weaviate backup file is too small." }
    Write-Log "    Weaviate backup OK: $WeaviateZip"
} catch {
    Write-Log "    Warning: Weaviate backup failed: $_"
}

# ───────────────────────────────────────────────────────
# 3. Storage Files Backup (uploaded docs, knowledge files)
# ───────────────────────────────────────────────────────
Write-Log "[3/5] Backing up storage files (knowledge base uploads)..."
$StorageZip = Join-Path $CurrentBackupFolder "dify_storage_$Date.zip"

try {
    if (Test-Path $VolumeStorage) {
        Compress-Archive -Path "$VolumeStorage\*" -DestinationPath $StorageZip -Force
        $StSize = (Get-Item $StorageZip).Length / 1MB
        Write-Log "    Storage backup OK: $StorageZip ($([math]::Round($StSize,2)) MB)"
    } else {
        Write-Log "    Warning: Storage volume not found at $VolumeStorage, skipping."
    }
} catch {
    Write-Log "    Warning: Storage backup failed: $_"
}

# ───────────────────────────────────────────────────────
# 4. Redis Backup (optional - cache & queue state)
# ───────────────────────────────────────────────────────
Write-Log "[4/5] Backing up Redis..."
$RedisBackup = Join-Path $CurrentBackupFolder "dify_redis_$Date.rdb"

try {
    if ($RedisContainer -in $RunningContainers) {
        docker exec $RedisContainer redis-cli SAVE
        docker cp "${RedisContainer}:/data/dump.rdb" $RedisBackup
        $RdSize = (Get-Item $RedisBackup).Length / 1KB
        Write-Log "    Redis backup OK: $RedisBackup ($([math]::Round($RdSize,2)) KB)"
    } else {
        Write-Log "    Warning: Redis container not running, skipping."
    }
} catch {
    Write-Log "    Warning: Redis backup failed: $_"
}

# ───────────────────────────────────────────────────────
# 5. .env File Backup (API keys, model settings)
# ───────────────────────────────────────────────────────
Write-Log "[5/5] Backing up .env configuration..."
$EnvBackup = Join-Path $CurrentBackupFolder "dify_env_$Date.env"

try {
    if (Test-Path $EnvFile) {
        Copy-Item $EnvFile $EnvBackup
        Write-Log "    .env backup OK: $EnvBackup"
    } else {
        Write-Log "    Warning: .env file not found at $EnvFile, skipping."
    }
} catch {
    Write-Log "    Warning: .env backup failed: $_"
}

# ───────────────────────────────────────────────────────
# Cleanup old backups (older than RetentionDays)
# ───────────────────────────────────────────────────────
Write-Log "Cleaning up backups older than $RetentionDays days..."
$LimitDate = (Get-Date).AddDays(-$RetentionDays)

# Cleanup sub-directories and loose files from old versions
$OldItems = Get-ChildItem -Path $BackupDir |
    Where-Object {
        $_.LastWriteTime -lt $LimitDate -and $_.Name -ne "README.md" -and $_.Name -ne "backup_log.txt"
    }

foreach ($Item in $OldItems) {
    Write-Log "    Deleting: $($Item.Name)"
    Remove-Item $Item.FullName -Recurse -Force
}

# ───────────────────────────────────────────────────────
# Summary Report
# ───────────────────────────────────────────────────────
$TotalSize = (Get-ChildItem -Path $BackupDir -File | Measure-Object -Property Length -Sum).Sum / 1MB
Write-Log "✅ Dify full backup completed successfully."
Write-Log "📊 Current backup folder total size: $([math]::Round($TotalSize, 2)) MB"
Write-Log "====== Backup End ======"
