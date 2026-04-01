# Dify Full Backup Script - LOCAL Environment (Windows PowerShell)
# Target: Local Docker Dify (docker-db_postgres-1, docker-weaviate-1, etc.)
# Backup output: C:\VSCode_Proj\Dify\backups\local\<timestamp>\
# Creator: Antigravity AI & Porter

$BackupRoot = "C:\VSCode_Proj\Dify\backups\local"
$Date       = Get-Date -Format "yyyyMMdd_HHmmss"
$LogFile    = "C:\VSCode_Proj\Dify\backups\local\backup_log.txt"
$RetentionDays = 7

# Dify Source Paths (Bind Mounts)
$DifyDockerRoot = "C:\VSCode_Proj\Dify\dify\docker"
$VolumeStorage  = "$DifyDockerRoot\volumes\app\storage"
$EnvFile        = "$DifyDockerRoot\.env"

# Container names (local docker)
$DbContainer    = "docker-db_postgres-1"
$WeaviateContainer = "docker-weaviate-1"
$RedisContainer = "docker-redis-1"
$DbUser = "postgres"
$DbName = "dify"

# ── Init ──────────────────────────────────────────────────────
if (!(Test-Path $BackupRoot)) { New-Item -ItemType Directory -Path $BackupRoot | Out-Null }

$CurrentBackupFolder = Join-Path $BackupRoot $Date
New-Item -ItemType Directory -Path $CurrentBackupFolder | Out-Null

function Write-Log {
    param([string]$Message)
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $FormattedMessage = "[$Timestamp] $Message"
    Write-Host $FormattedMessage
    $FormattedMessage | Out-File -FilePath $LogFile -Append -Encoding utf8
}

Write-Log "====== [LOCAL] Dify Full Backup Start ======"
Write-Log "Backup target folder: $CurrentBackupFolder"

# Check DB container is running
$RunningContainers = docker ps --format "{{.Names}}"
if ($DbContainer -notin $RunningContainers) {
    Write-Log "Error: DB Container $DbContainer is not running. Aborting."
    exit 1
}

# ── 1. PostgreSQL ───────────────────────────────────────────
Write-Log "[1/5] Backing up PostgreSQL ($DbContainer)..."
$TempSqlFile  = "/tmp/dify_$Date.sql"
$LocalSqlFile = Join-Path $CurrentBackupFolder "dify_$Date.sql"
$PgZipFile    = Join-Path $CurrentBackupFolder "dify_postgres_$Date.zip"

try {
    docker exec $DbContainer pg_dump -U $DbUser -d $DbName -f $TempSqlFile
    docker cp "${DbContainer}:${TempSqlFile}" $LocalSqlFile
    docker exec $DbContainer rm $TempSqlFile

    if ((Get-Item $LocalSqlFile).Length -lt 10KB) { throw "PostgreSQL dump file is too small." }

    Compress-Archive -Path $LocalSqlFile -DestinationPath $PgZipFile -Force
    Remove-Item $LocalSqlFile
    $PgSize = [math]::Round((Get-Item $PgZipFile).Length / 1MB, 2)
    Write-Log "    PostgreSQL backup OK: $PgZipFile ($PgSize MB)"
} catch {
    Write-Log "Error: PostgreSQL backup failed! $_"
    exit 1
}

# ── 2. Weaviate ─────────────────────────────────────────────
Write-Log "[2/5] Backing up Weaviate vector store..."
$WeaviateZip = Join-Path $CurrentBackupFolder "dify_weaviate_$Date.zip"

try {
    $WeaviateTar = "/tmp/weaviate_backup_$Date.tar.gz"
    docker exec $WeaviateContainer sh -c "tar -czf $WeaviateTar /var/lib/weaviate 2>/dev/null"
    docker cp "${WeaviateContainer}:${WeaviateTar}" $WeaviateZip
    docker exec $WeaviateContainer rm $WeaviateTar

    if ((Get-Item $WeaviateZip).Length -lt 1MB) { throw "Weaviate backup file is too small." }
    $WvSize = [math]::Round((Get-Item $WeaviateZip).Length / 1MB, 2)
    Write-Log "    Weaviate backup OK: $WeaviateZip ($WvSize MB)"
} catch {
    Write-Log "    Warning: Weaviate backup failed: $_"
}

# ── 3. Storage ──────────────────────────────────────────────
Write-Log "[3/5] Backing up storage files (knowledge base uploads)..."
$StorageZip = Join-Path $CurrentBackupFolder "dify_storage_$Date.zip"

try {
    if (Test-Path $VolumeStorage) {
        Compress-Archive -Path "$VolumeStorage\*" -DestinationPath $StorageZip -Force
        $StSize = [math]::Round((Get-Item $StorageZip).Length / 1MB, 2)
        Write-Log "    Storage backup OK: $StorageZip ($StSize MB)"
    } else {
        Write-Log "    Warning: Storage volume not found at $VolumeStorage, skipping."
    }
} catch {
    Write-Log "    Warning: Storage backup failed: $_"
}

# ── 4. Redis ────────────────────────────────────────────────
Write-Log "[4/5] Backing up Redis..."
$RedisBackup = Join-Path $CurrentBackupFolder "dify_redis_$Date.rdb"

try {
    if ($RedisContainer -in $RunningContainers) {
        docker exec $RedisContainer redis-cli SAVE
        docker cp "${RedisContainer}:/data/dump.rdb" $RedisBackup
        $RdSize = [math]::Round((Get-Item $RedisBackup).Length / 1KB, 2)
        Write-Log "    Redis backup OK: $RedisBackup ($RdSize KB)"
    } else {
        Write-Log "    Warning: Redis container not running, skipping."
    }
} catch {
    Write-Log "    Warning: Redis backup failed: $_"
}

# ── 5. .env ─────────────────────────────────────────────────
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

# ── Cleanup old backups ────────────────────────────────────
Write-Log "Cleaning up backups older than $RetentionDays days..."
$LimitDate = (Get-Date).AddDays(-$RetentionDays)
$OldItems = Get-ChildItem -Path $BackupRoot |
    Where-Object {
        $_.LastWriteTime -lt $LimitDate -and
        $_.Name -ne "README.md" -and
        $_.Name -ne "backup_log.txt"
    }
foreach ($Item in $OldItems) {
    Write-Log "    Deleting: $($Item.Name)"
    Remove-Item $Item.FullName -Recurse -Force
}

# ── Summary ─────────────────────────────────────────────────
$TotalSize = (Get-ChildItem -Path $BackupRoot -Recurse -File |
    Where-Object { $_.Name -ne "backup_log.txt" } |
    Measure-Object -Property Length -Sum).Sum / 1MB
Write-Log "✅ [LOCAL] Dify full backup completed successfully."
Write-Log "📊 Total backup size (local): $([math]::Round($TotalSize, 2)) MB"
Write-Log "====== Backup End ======"
