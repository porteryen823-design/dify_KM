# Dify Full Restore Script (Windows PowerShell)
# Logic: Mandatory Safety Backup -> User Confirmation -> Automated Restore
# Creator: Antigravity AI & Porter

param (
    [Parameter(Mandatory=$true)]
    [string]$TargetFolder,  # Target backup folder
    [switch]$Force           # Skip confirmation
)

$BackupScript = "C:\VSCode_Proj\Dify\scripts\backup-dify.ps1"
$DifyDockerRoot = "C:\VSCode_Proj\Dify\dify\docker"
$LogFile = "C:\VSCode_Proj\Dify\backups\restore_log.txt"

function Write-Log {
    param([string]$Message)
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $FormattedMessage = "[$Timestamp] $Message"
    Write-Host $FormattedMessage
    $FormattedMessage | Out-File -FilePath $LogFile -Append -Encoding utf8
}

Write-Log "====== Dify Restore Process Started ======"

# 1. Verify source folder
if (!(Test-Path $TargetFolder)) {
    Write-Log "Error: Target folder $TargetFolder not found."
    exit 1
}

# 2. Safety Backup (Pre-Restore Snapshot)
Write-Log "Safety: Creating pre-restore backup..."
powershell.exe -ExecutionPolicy Bypass -File $BackupScript
if ($LASTEXITCODE -ne 0) {
    Write-Log "Error: Safety backup failed (Exit Code $LASTEXITCODE). Aborting restore to protect current data."
    exit 1
}
Write-Log "Safety: Pre-restore backup completed."

# 3. Confirmation
if (!$Force) {
    Write-Log "WARNING: This will overwrite your current Dify data with: $TargetFolder"
    $Confirm = Read-Host "Are you sure? (Y/N)"
    if ($Confirm -ne "Y") {
        Write-Log "User cancelled restore."
        exit 0
    }
} else {
    Write-Log "Force flag detected. Skipping confirmation."
}

Write-Log "Starting restoration..."

# 4. Preparation
$TempDir = Join-Path $TargetFolder "restore_tmp"
if (Test-Path $TempDir) { Remove-Item $TempDir -Recurse -Force }
$null = New-Item -ItemType Directory -Path $TempDir

# 5. Restore .env
$EnvBackup = Get-ChildItem -Path $TargetFolder -Filter "dify_env_*.env" | Select-Object -First 1
if ($EnvBackup) {
    Write-Log "[1/5] Restoring .env..."
    Copy-Item $EnvBackup.FullName (Join-Path $DifyDockerRoot ".env") -Force
}

# 6. Restore PostgreSQL
$PgZip = Get-ChildItem -Path $TargetFolder -Filter "dify_postgres_*.zip" | Select-Object -First 1
if ($PgZip) {
    Write-Log "[2/5] Restoring PostgreSQL..."
    Expand-Archive -Path $PgZip.FullName -DestinationPath $TempDir -Force
    $SqlFile = Get-ChildItem -Path $TempDir -Filter "*.sql" | Select-Object -First 1
    
    # Wait for PostgreSQL to be ready
    Write-Log "    Waiting for PostgreSQL to be ready..."
    $retryCount = 0
    while ($retryCount -lt 12) {
        $check = docker exec docker-db_postgres-1 pg_isready -U postgres 2>&1
        if ($LASTEXITCODE -eq 0) { break }
        Write-Log "    PostgreSQL not ready, waiting 5s... ($($retryCount+1)/12)"
        Start-Sleep -Seconds 5
        $retryCount++
    }

    # Drop schema to ensure clean slate
    docker exec docker-db_postgres-1 psql -U postgres -d dify -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
    docker cp $SqlFile.FullName "docker-db_postgres-1:/tmp/restore.sql"
    docker exec docker-db_postgres-1 psql -U postgres -d dify -f /tmp/restore.sql
}

# 7. Restore Weaviate
$WvBackup = Get-ChildItem -Path $TargetFolder -Filter "dify_weaviate_*" | Select-Object -First 1
if ($WvBackup) {
    Write-Log "[3/5] Restoring Weaviate..."
    docker cp $WvBackup.FullName "docker-weaviate-1:/tmp/restore_wv.tar.gz"
    docker exec docker-weaviate-1 sh -c "rm -rf /var/lib/weaviate/* && tar -xzf /tmp/restore_wv.tar.gz -C /"
    Write-Log "    Weaviate files restored."
}

# 8. Restore Storage
$StorageZip = Get-ChildItem -Path $TargetFolder -Filter "dify_storage_*.zip" | Select-Object -First 1
if ($StorageZip) {
    Write-Log "[4/5] Restoring Storage..."
    $StoragePath = "C:\VSCode_Proj\Dify\dify\docker\volumes\app\storage"
    if (Test-Path $StoragePath) {
        Get-ChildItem -Path $StoragePath | Remove-Item -Recurse -Force
    }
    Expand-Archive -Path $StorageZip.FullName -DestinationPath $StoragePath -Force
}

# 9. Restore Redis
$RedisRdb = Get-ChildItem -Path $TargetFolder -Filter "dify_redis_*.rdb" | Select-Object -First 1
if ($RedisRdb) {
    Write-Log "[5/5] Restoring Redis..."
    docker stop docker-redis-1
    docker cp $RedisRdb.FullName "docker-redis-1:/data/dump.rdb"
    docker start docker-redis-1
}

# 10. Restart and Cleanup
if (Test-Path $TempDir) { Remove-Item $TempDir -Recurse -Force }
Write-Log "Restarting Dify services..."
docker compose -f (Join-Path $DifyDockerRoot "docker-compose.yaml") restart

Write-Log "Restoration completed successfully."
Write-Log "====== Restore End ======"
