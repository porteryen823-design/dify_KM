# Dify Full Restore Script - AWS GYRO Environment (Windows PowerShell)
# Logic: Safety Backup (local snapshot) -> User Confirmation -> Push backup files to EC2 -> Restore remotely
# Source: backups\dify-aws-gyro\<timestamp>\
# Creator: Antigravity AI & Porter

param (
    [Parameter(Mandatory=$true)]
    [string]$TargetFolder,   # e.g. C:\VSCode_Proj\Dify\backups\dify-aws-gyro\20260331_103602
    [switch]$Force           # Skip interactive confirmation
)

# ── SSH / Remote Config ─────────────────────────────────────
$SshHost      = "dify-aws-gyro"
$RemoteBase   = "/home/ubuntu/Dify/dify/docker"
$RemoteTmpDir = "/tmp/dify_restore_gyro"

$RemoteDbContainer      = "docker-db_postgres-1"
$RemoteWeaviateContainer= "docker-weaviate-1"
$RemoteRedisContainer   = "docker-redis-1"
$RemoteDbUser = "postgres"
$RemoteDbName = "dify"

# ── Local Config ────────────────────────────────────────────
$BackupScript = "C:\VSCode_Proj\Dify\scripts\backup-dify-aws-gyro.ps1"
$LogFile      = "C:\VSCode_Proj\Dify\backups\dify-aws-gyro\restore_log.txt"

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

Write-Log "====== [GYRO/AWS] Dify Restore Process Started ======"

# ── 1. Verify source folder ─────────────────────────────────
if (!(Test-Path $TargetFolder)) {
    Write-Log "Error: Target folder '$TargetFolder' not found."
    exit 1
}
Write-Log "Restore source: $TargetFolder"

# ── 2. Test SSH Connection ──────────────────────────────────
Write-Log "Testing SSH connection to $SshHost..."
$null = Invoke-SSH "echo 'SSH_OK'"
if ($LASTEXITCODE -ne 0) {
    Write-Log "Error: Cannot connect to $SshHost via SSH. Check ~/.ssh/config. Aborting."
    exit 1
}
Write-Log "    SSH connection OK."

# ── 3. Safety Backup (Pre-Restore Remote Snapshot) ──────────
Write-Log "Safety: Creating pre-restore backup of AWS GYRO current state..."
powershell.exe -ExecutionPolicy Bypass -File $BackupScript
if ($LASTEXITCODE -ne 0) {
    Write-Log "Error: Safety backup failed (Exit Code $LASTEXITCODE). Aborting to protect current data."
    exit 1
}
Write-Log "Safety: Pre-restore backup completed."

# ── 4. User Confirmation ─────────────────────────────────────
if (!$Force) {
    Write-Log "WARNING: This will OVERWRITE the REMOTE Dify data on $SshHost."
    Write-Log "         Restore source: $TargetFolder"
    $Confirm = Read-Host "Are you sure? (Y/N)"
    if ($Confirm -ne "Y") {
        Write-Log "User cancelled restore."
        exit 0
    }
} else {
    Write-Log "Force flag detected. Skipping confirmation."
}

Write-Log "Starting remote restoration on $SshHost..."

# ── Prepare remote temp workspace ───────────────────────────
Write-Log "Stopping Dify application containers (API, Web, Worker, etc.) to prevent database locks..."
Invoke-SSH "cd $RemoteBase && docker compose stop api worker worker_beat plugin_daemon web nginx sandbox ssrf_proxy" | Out-Null
Invoke-SSH "rm -rf $RemoteTmpDir && mkdir -p $RemoteTmpDir" | Out-Null

# ── [1/5] Restore .env ──────────────────────────────────────
$EnvBackup = Get-ChildItem -Path $TargetFolder -Filter "dify_env_*.env" | Select-Object -First 1
if ($EnvBackup) {
    Write-Log "[1/5] Restoring .env to $SshHost..."
    scp "$($EnvBackup.FullName)" "${SshHost}:${RemoteBase}/.env"
    if ($LASTEXITCODE -eq 0) {
        Write-Log "    .env restored to $RemoteBase/.env"
    } else {
        Write-Log "    Warning: .env restore failed."
    }
} else {
    Write-Log "[1/5] Warning: No .env backup found, skipping."
}

# ── [2/5] Restore PostgreSQL ────────────────────────────────
$PgZip = Get-ChildItem -Path $TargetFolder | Where-Object { $_.Name -match "dify_postgres_.*(\.zip|\.tar\.gz)" } | Select-Object -First 1
if ($PgZip) {
    Write-Log "[2/5] Restoring PostgreSQL on $SshHost..."

    # Upload compressed archive
    $RemotePgTar = "$RemoteTmpDir/restore_pg.tar.gz"
    scp "$($PgZip.FullName)" "${SshHost}:${RemotePgTar}"

    # Extract on remote -> get .sql -> restore
    Invoke-SSH "cd $RemoteTmpDir && tar -xzf restore_pg.tar.gz" | Out-Null
    $null = Invoke-SSH "ls $RemoteTmpDir/*.sql > /dev/null 2>&1"

    if ($LASTEXITCODE -eq 0) {
        # Wait for PostgreSQL readiness
        Write-Log "    Waiting for PostgreSQL to be ready..."
        $retryCount = 0
        while ($retryCount -lt 12) {
            $null = Invoke-SSH "docker exec $RemoteDbContainer pg_isready -U $RemoteDbUser"
            if ($LASTEXITCODE -eq 0) { break }
            Write-Log "    PostgreSQL not ready, waiting 5s... ($($retryCount+1)/12)"
            Start-Sleep -Seconds 5
            $retryCount++
        }

        Invoke-SSH "docker exec $RemoteDbContainer psql -U $RemoteDbUser -d $RemoteDbName -c 'DROP SCHEMA public CASCADE; CREATE SCHEMA public;'" | Out-Null
        Invoke-SSH "RESTORE_SQL=\$(ls $RemoteTmpDir/*.sql | head -1); docker cp ""\$RESTORE_SQL"" ${RemoteDbContainer}:/tmp/restore.sql" | Out-Null
        Invoke-SSH "docker exec $RemoteDbContainer psql -U $RemoteDbUser -d $RemoteDbName -f /tmp/restore.sql" | Out-Null
        Write-Log "    PostgreSQL restored."
    } else {
        Write-Log "    Warning: Cannot find SQL file after extraction, skipping."
    }
} else {
    Write-Log "[2/5] Warning: No PostgreSQL backup found, skipping."
}

# ── [3/5] Restore Weaviate ───────────────────────────────────
$WvBackup = Get-ChildItem -Path $TargetFolder | Where-Object { $_.Name -match "dify_weaviate_.*(\.zip|\.tar\.gz)" } | Select-Object -First 1
if ($WvBackup) {
    Write-Log "[3/5] Restoring Weaviate on $SshHost..."
    $RemoteWvFile = "$RemoteTmpDir/restore_wv.tar.gz"
    scp "$($WvBackup.FullName)" "${SshHost}:${RemoteWvFile}"
    Invoke-SSH "docker cp $RemoteWvFile ${RemoteWeaviateContainer}:/tmp/restore_wv.tar.gz" | Out-Null
    Invoke-SSH "docker exec $RemoteWeaviateContainer sh -c 'rm -rf /var/lib/weaviate/* && tar -xzf /tmp/restore_wv.tar.gz -C /'" | Out-Null
    Write-Log "    Weaviate restored."
} else {
    Write-Log "[3/5] Warning: No Weaviate backup found, skipping."
}

# ── [4/5] Restore Storage ────────────────────────────────────
$StorageZip = Get-ChildItem -Path $TargetFolder | Where-Object { $_.Name -match "dify_storage_.*(\.zip|\.tar\.gz)" } | Select-Object -First 1
if ($StorageZip) {
    Write-Log "[4/5] Restoring Storage on $SshHost..."
    $RemoteStorageDir = "$RemoteBase/volumes/app/storage"
    $RemoteStorageTar = "$RemoteTmpDir/restore_storage.tar.gz"
    scp "$($StorageZip.FullName)" "${SshHost}:${RemoteStorageTar}"
    Invoke-SSH "sudo rm -rf ${RemoteStorageDir}/* && sudo mkdir -p $RemoteStorageDir" | Out-Null
    # untar on remote (using sudo because docker volume contents may be root-owned)
    Invoke-SSH "sudo tar -xzf $RemoteStorageTar -C $RemoteStorageDir" | Out-Null
    Write-Log "    Storage restored."
} else {
    Write-Log "[4/5] Warning: No Storage backup found, skipping."
}

# ── [5/5] Restore Redis ──────────────────────────────────────
$RedisRdb = Get-ChildItem -Path $TargetFolder -Filter "dify_redis_*.rdb" | Select-Object -First 1
if ($RedisRdb) {
    Write-Log "[5/5] Restoring Redis on $SshHost..."
    $RemoteRdbFile = "$RemoteTmpDir/restore.rdb"
    scp "$($RedisRdb.FullName)" "${SshHost}:${RemoteRdbFile}"
    Invoke-SSH "docker stop $RemoteRedisContainer" | Out-Null
    Invoke-SSH "docker cp $RemoteRdbFile ${RemoteRedisContainer}:/data/dump.rdb" | Out-Null
    Invoke-SSH "docker start $RemoteRedisContainer" | Out-Null
    Write-Log "    Redis restored."
} else {
    Write-Log "[5/5] Warning: No Redis backup found, skipping."
}

# ── Cleanup & Restart ─────────────────────────────────────────
Invoke-SSH "rm -rf $RemoteTmpDir" | Out-Null
Write-Log "Restarting Dify services on $SshHost..."
Invoke-SSH "cd $RemoteBase && docker compose restart"

Write-Log "✅ [GYRO/AWS] Remote restoration completed successfully."
Write-Log "====== Restore End ======"
