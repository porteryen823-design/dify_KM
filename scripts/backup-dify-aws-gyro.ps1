# Dify Backup Script - AWS GYRO Environment (Windows PowerShell)
# Target: Remote Dify on AWS EC2 (dify-aws-gyro), connected via SSH
# Strategy: SSH into EC2 -> run pg_dump/tar inside containers -> scp back to local
# Backup output: C:\VSCode_Proj\Dify\backups\dify-aws-gyro\<timestamp>\
# Creator: Antigravity AI & Porter

# ── SSH / Remote Config ────────────────────────────────────
$SshHost      = "dify-aws-gyro"               # Matches ~/.ssh/config Host entry
$RemoteBase   = "/home/ubuntu/Dify/dify/docker" # Dify docker-compose root on EC2
$RemoteTmpDir = "/tmp/dify_backup_gyro"

# Container names on the remote host (adjust if different)
$RemoteDbContainer      = "docker-db_postgres-1"
$RemoteWeaviateContainer= "docker-weaviate-1"
$RemoteRedisContainer   = "docker-redis-1"
$RemoteDbUser = "postgres"
$RemoteDbName = "dify"

# ── Local Config ───────────────────────────────────────────
$BackupRoot = "C:\VSCode_Proj\Dify\backups\dify-aws-gyro"
$Date       = Get-Date -Format "yyyyMMdd_HHmmss"
$LogFile    = "C:\VSCode_Proj\Dify\backups\dify-aws-gyro\backup_log.txt"
$RetentionDays = 14  # AWS 備份保留更長 (14 天)

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

function Invoke-SSH {
    param([string]$Command)
    ssh $SshHost $Command
    return $LASTEXITCODE
}

Write-Log "====== [GYRO/AWS] Dify Full Backup Start ======"
Write-Log "Remote host: $SshHost"
Write-Log "Backup target folder: $CurrentBackupFolder"

# ── Test SSH Connection ────────────────────────────────────
Write-Log "Testing SSH connection to $SshHost..."
$null = Invoke-SSH "echo 'SSH_OK'"
if ($LASTEXITCODE -ne 0) {
    Write-Log "Error: Cannot connect to $SshHost via SSH. Check ~/.ssh/config. (ExitCode: $LASTEXITCODE). Aborting."
    exit 1
}
Write-Log "    SSH connection OK."

# ── Prepare remote temp directory ─────────────────────────
Invoke-SSH "mkdir -p $RemoteTmpDir" | Out-Null

# ── 1. PostgreSQL ───────────────────────────────────────────
Write-Log "[1/5] Backing up PostgreSQL on $SshHost ($RemoteDbContainer)..."
$RemoteSqlFile  = "$RemoteTmpDir/dify_$Date.sql"
$RemotePgTar    = "$RemoteTmpDir/dify_postgres_$Date.tar.gz"
$LocalPgZip     = Join-Path $CurrentBackupFolder "dify_postgres_$Date.tar.gz"

try {
    # Dump inside container -> copy out -> compress
    Invoke-SSH "docker exec $RemoteDbContainer pg_dump -U $RemoteDbUser -d $RemoteDbName -f /tmp/dify_dump_$Date.sql" | Out-Null
    Invoke-SSH "docker cp ${RemoteDbContainer}:/tmp/dify_dump_$Date.sql $RemoteSqlFile" | Out-Null
    Invoke-SSH "docker exec $RemoteDbContainer rm /tmp/dify_dump_$Date.sql" | Out-Null
    Invoke-SSH "tar -czf $RemotePgTar -C $RemoteTmpDir dify_$Date.sql" | Out-Null

    # SCP down
    scp "${SshHost}:${RemotePgTar}" "$LocalPgZip"

    if (!(Test-Path $LocalPgZip) -or (Get-Item $LocalPgZip).Length -lt 1KB) {
        throw "Downloaded PostgreSQL backup is missing or too small."
    }
    $PgSize = [math]::Round((Get-Item $LocalPgZip).Length / 1MB, 2)
    Write-Log "    PostgreSQL backup OK: $LocalPgZip ($PgSize MB)"
} catch {
    Write-Log "Error: PostgreSQL backup failed! $_"
    # Cleanup remote before exit
    Invoke-SSH "rm -rf $RemoteTmpDir" | Out-Null
    exit 1
}

# ── 2. Weaviate ─────────────────────────────────────────────
Write-Log "[2/5] Backing up Weaviate vector store on $SshHost..."
$RemoteWvTar = "$RemoteTmpDir/dify_weaviate_$Date.tar.gz"
$LocalWvFile = Join-Path $CurrentBackupFolder "dify_weaviate_$Date.tar.gz"

try {
    Invoke-SSH "docker exec $RemoteWeaviateContainer sh -c 'tar -czf /tmp/wv_backup.tar.gz /var/lib/weaviate 2>/dev/null'" | Out-Null
    Invoke-SSH "docker cp ${RemoteWeaviateContainer}:/tmp/wv_backup.tar.gz $RemoteWvTar" | Out-Null
    Invoke-SSH "docker exec $RemoteWeaviateContainer rm /tmp/wv_backup.tar.gz" | Out-Null

    scp "${SshHost}:${RemoteWvTar}" "$LocalWvFile"

    if (!(Test-Path $LocalWvFile) -or (Get-Item $LocalWvFile).Length -lt 1MB) {
        throw "Weaviate backup is too small."
    }
    $WvSize = [math]::Round((Get-Item $LocalWvFile).Length / 1MB, 2)
    Write-Log "    Weaviate backup OK: $LocalWvFile ($WvSize MB)"
} catch {
    Write-Log "    Warning: Weaviate backup failed: $_"
}

# ── 3. Storage ──────────────────────────────────────────────
Write-Log "[3/5] Backing up Storage files on $SshHost..."
$RemoteStorageDir = "$RemoteBase/volumes/app/storage"
$RemoteStorageTar = "$RemoteTmpDir/dify_storage_$Date.tar.gz"
$LocalStorageFile = Join-Path $CurrentBackupFolder "dify_storage_$Date.tar.gz"

try {
    Invoke-SSH "tar -czf $RemoteStorageTar -C $RemoteStorageDir ." | Out-Null
    scp "${SshHost}:${RemoteStorageTar}" "$LocalStorageFile"

    if (!(Test-Path $LocalStorageFile)) { throw "Storage backup download failed." }
    $StSize = [math]::Round((Get-Item $LocalStorageFile).Length / 1MB, 2)
    Write-Log "    Storage backup OK: $LocalStorageFile ($StSize MB)"
} catch {
    Write-Log "    Warning: Storage backup failed: $_"
}

# ── 4. Redis ────────────────────────────────────────────────
Write-Log "[4/5] Backing up Redis on $SshHost..."
$RemoteRdb     = "$RemoteTmpDir/dify_redis_$Date.rdb"
$LocalRedisFile= Join-Path $CurrentBackupFolder "dify_redis_$Date.rdb"

try {
    Invoke-SSH "docker exec $RemoteRedisContainer redis-cli SAVE" | Out-Null
    Invoke-SSH "docker cp ${RemoteRedisContainer}:/data/dump.rdb $RemoteRdb" | Out-Null
    scp "${SshHost}:${RemoteRdb}" "$LocalRedisFile"

    if (!(Test-Path $LocalRedisFile)) { throw "Redis backup download failed." }
    $RdSize = [math]::Round((Get-Item $LocalRedisFile).Length / 1KB, 2)
    Write-Log "    Redis backup OK: $LocalRedisFile ($RdSize KB)"
} catch {
    Write-Log "    Warning: Redis backup failed: $_"
}

# ── 5. .env ─────────────────────────────────────────────────
Write-Log "[5/5] Backing up .env from $SshHost..."
$RemoteEnvFile = "$RemoteBase/.env"
$LocalEnvFile  = Join-Path $CurrentBackupFolder "dify_env_$Date.env"

try {
    scp "${SshHost}:${RemoteEnvFile}" "$LocalEnvFile"
    if (!(Test-Path $LocalEnvFile)) { throw ".env download failed." }
    Write-Log "    .env backup OK: $LocalEnvFile"
} catch {
    Write-Log "    Warning: .env backup failed: $_"
}

# ── Cleanup remote temp ────────────────────────────────────
Write-Log "Cleaning up remote temp files..."
Invoke-SSH "rm -rf $RemoteTmpDir" | Out-Null

# ── Cleanup old local backups ──────────────────────────────
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
Write-Log "✅ [GYRO/AWS] Dify full backup completed successfully."
Write-Log "📊 Total backup size (dify-aws-gyro): $([math]::Round($TotalSize, 2)) MB"
Write-Log "====== Backup End ======"
