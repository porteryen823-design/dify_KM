for ($i = 1; $i -le 3; $i++) {
    Write-Output "--- Starting Restore Attempt #$i ---"
    & powershell.exe -ExecutionPolicy Bypass -File C:\VSCode_Proj\Dify\scripts\restore-dify.ps1 -TargetFolder "C:\VSCode_Proj\Dify\backups\20260317_105257" -Force
    if ($i -lt 3) {
        Write-Output "Waiting 30 seconds..."
        Start-Sleep -Seconds 30
    }
}
Write-Output "=== 3-Run Sequence Completed ==="
