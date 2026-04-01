# Dify Full Restore Script - LOCAL Environment (Windows PowerShell)
# Logic: Safety Backup -> User Confirmation -> Restore (PostgreSQL, Weaviate, Storage, Redis, .env)
# Source: backups\local\<timestamp>\
# Creator: Antigravity AI & Porter

param (
    [Parameter(Mandatory=$true)]
    [string]$TargetFolder,   # e.g. C:\VSCode_Proj\Dify\backups\local\20260331_103602
    [switch]$Force           # Skip interactive confirmation
)

$BackupScript   = "C:\VSCode_Proj\Dify\scripts\backup-dify-local.ps1"
$DifyDockerRoot = "C:\VSCode_Proj\Dify\dify\docker"
$LogFile        = "C:\VSCode_Proj\Dify\backups\local\restore_log.txt"

$DbContainer      = "docker-db_postgres-1"
$WeaviateContainer= "docker-weaviate-1"
$RedisContainer   = "docker-redis-1"
$DbUser           = "postgres"
$DbName           = "dify"

function Write-Log {
    param([string]$Message)
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $FormattedMessage = "[$Timestamp] $Message"
    Write-Host $FormattedMessage
    $FormattedMessage | Out-File -FilePath $LogFile -Append -Encoding utf8
}

Write-Log "====== [LOCAL] Dify Restore Process Started ======"

# ── 1. Verify source folder ─────────────────────────────────
if (!(Test-Path $TargetFolder)) {
    Write-Log "Error: Target folder '$TargetFolder' not found."
    exit 1
}
Write-Log "Restore source: $TargetFolder"

# ── 2. Safety Backup (Pre-Restore Snapshot) ─────────────────
Write-Log "Safety: Creating pre-restore backup of current LOCAL state..."
powershell.exe -ExecutionPolicy Bypass -File $BackupScript
if ($LASTEXITCODE -ne 0) {
    Write-Log "Error: Safety backup failed (Exit Code $LASTEXITCODE). Aborting to protect current data."
    exit 1
}
Write-Log "Safety: Pre-restore backup completed."

# ── 3. User Confirmation ────────────────────────────────────
if (!$Force) {
    Write-Log "WARNING: This will OVERWRITE your current LOCAL Dify data."
    Write-Log "         Restore source: $TargetFolder"
    $Confirm = Read-Host "Are you sure? (Y/N)"
    if ($Confirm -ne "Y") {
        Write-Log "User cancelled restore."
        exit 0
    }
} else {
    Write-Log "Force flag detected. Skipping confirmation."
}

Write-Log "Starting local restoration..."

# ── Temp workspace ──────────────────────────────────────────
$TempDir = Join-Path $TargetFolder "restore_tmp"
if (Test-Path $TempDir) { Remove-Item $TempDir -Recurse -Force }
$null = New-Item -ItemType Directory -Path $TempDir

# ── [1/5] Restore .env ─────────────────────────────────────
$EnvBackup = Get-ChildItem -Path $TargetFolder -Filter "dify_env_*.env" | Select-Object -First 1
if ($EnvBackup) {
    Write-Log "[1/5] Restoring .env..."
    Copy-Item $EnvBackup.FullName (Join-Path $DifyDockerRoot ".env") -Force
    Write-Log "    .env restored to $DifyDockerRoot\.env"
} else {
    Write-Log "[1/5] Warning: No .env backup found, skipping."
}

# ── [2/5] Restore PostgreSQL ────────────────────────────────
$PgZip = Get-ChildItem -Path $TargetFolder -Filter "dify_postgres_*.zip" | Select-Object -First 1
if ($PgZip) {
    Write-Log "[2/5] Restoring PostgreSQL..."
    Expand-Archive -Path $PgZip.FullName -DestinationPath $TempDir -Force
    $SqlFile = Get-ChildItem -Path $TempDir -Filter "*.sql" | Select-Object -First 1

    Write-Log "    Waiting for PostgreSQL to be ready..."
    $retryCount = 0
    while ($retryCount -lt 12) {
        $null = docker exec $DbContainer pg_isready -U $DbUser 2>&1
        if ($LASTEXITCODE -eq 0) { break }
        Write-Log "    PostgreSQL not ready, waiting 5s... ($($retryCount+1)/12)"
        Start-Sleep -Seconds 5
        $retryCount++
    }

    docker exec $DbContainer psql -U $DbUser -d $DbName -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
    docker cp $SqlFile.FullName "${DbContainer}:/tmp/restore.sql"
    docker exec $DbContainer psql -U $DbUser -d $DbName -f /tmp/restore.sql
    Write-Log "    PostgreSQL restored."
} else {
    Write-Log "[2/5] Warning: No PostgreSQL backup found, skipping."
}

# ── [3/5] Restore Weaviate ──────────────────────────────────
$WvBackup = Get-ChildItem -Path $TargetFolder -Filter "dify_weaviate_*" | Select-Object -First 1
if ($WvBackup) {
    Write-Log "[3/5] Restoring Weaviate..."
    docker cp $WvBackup.FullName "${WeaviateContainer}:/tmp/restore_wv.tar.gz"
    docker exec $WeaviateContainer sh -c "rm -rf /var/lib/weaviate/* && tar -xzf /tmp/restore_wv.tar.gz -C /"
    Write-Log "    Weaviate restored."
} else {
    Write-Log "[3/5] Warning: No Weaviate backup found, skipping."
}

# ── [4/5] Restore Storage ───────────────────────────────────
$StorageZip = Get-ChildItem -Path $TargetFolder -Filter "dify_storage_*.zip" | Select-Object -First 1
if ($StorageZip) {
    Write-Log "[4/5] Restoring Storage..."
    $StoragePath = "$DifyDockerRoot\volumes\app\storage"
    if (Test-Path $StoragePath) { Get-ChildItem -Path $StoragePath | Remove-Item -Recurse -Force }
    else { New-Item -ItemType Directory -Path $StoragePath | Out-Null }
    Expand-Archive -Path $StorageZip.FullName -DestinationPath $StoragePath -Force
    Write-Log "    Storage restored."
} else {
    Write-Log "[4/5] Warning: No Storage backup found, skipping."
}

# ── [5/5] Restore Redis ─────────────────────────────────────
$RedisRdb = Get-ChildItem -Path $TargetFolder -Filter "dify_redis_*.rdb" | Select-Object -First 1
if ($RedisRdb) {
    Write-Log "[5/5] Restoring Redis..."
    docker stop $RedisContainer
    docker cp $RedisRdb.FullName "${RedisContainer}:/data/dump.rdb"
    docker start $RedisContainer
    Write-Log "    Redis restored."
} else {
    Write-Log "[5/5] Warning: No Redis backup found, skipping."
}

# ── Cleanup & Restart ───────────────────────────────────────
if (Test-Path $TempDir) { Remove-Item $TempDir -Recurse -Force }
Write-Log "Restarting local Dify services..."
docker compose -f (Join-Path $DifyDockerRoot "docker-compose.yaml") restart

Write-Log "✅ [LOCAL] Restoration completed successfully."
Write-Log "====== Restore End ======"
