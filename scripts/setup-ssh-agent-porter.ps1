# ================================================================
# setup-ssh-agent-porter.ps1
# 目的：啟動 OpenSSH Authentication Agent 並載入 dify-aws-porter 的 PEM key
# ⚠️ 必須以「系統管理員」身份執行此腳本（一次性設定）
# ================================================================

$PemPath = "C:\Users\porte\Downloads\dify_ubuntu2.pem"
$ContextName = "dify-aws-porter"

Write-Host "=== Dify AWS Porter SSH Agent Setup ===" -ForegroundColor Cyan

# Step 1: 設定 ssh-agent 為自動啟動
Write-Host "`n[1/4] 設定 ssh-agent 自動啟動..." -ForegroundColor Yellow
try {
    Set-Service -Name ssh-agent -StartupType Automatic -ErrorAction Stop
    Write-Host "    OK: StartupType 設為 Automatic" -ForegroundColor Green
} catch {
    Write-Host "    ERROR: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "    請確認以管理員身份執行本腳本！" -ForegroundColor Red
    exit 1
}

# Step 2: 啟動 ssh-agent 服務
Write-Host "`n[2/4] 啟動 ssh-agent 服務..." -ForegroundColor Yellow
try {
    Start-Service ssh-agent -ErrorAction Stop
    Write-Host "    OK: ssh-agent 服務已啟動" -ForegroundColor Green
} catch {
    Write-Host "    ERROR: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Step 3: 載入 PEM key
Write-Host "`n[3/4] 載入 PEM key: $PemPath" -ForegroundColor Yellow
if (-not (Test-Path $PemPath)) {
    Write-Host "    ERROR: PEM 檔案不存在: $PemPath" -ForegroundColor Red
    exit 1
}
ssh-add $PemPath
if ($LASTEXITCODE -eq 0) {
    Write-Host "    OK: PEM key 已載入" -ForegroundColor Green
} else {
    Write-Host "    ERROR: ssh-add 失敗" -ForegroundColor Red
    exit 1
}

# Step 4: 顯示已載入的 keys
Write-Host "`n[4/4] 已載入的 SSH Keys：" -ForegroundColor Yellow
ssh-add -l

Write-Host "`n=== 設定完成！===" -ForegroundColor Cyan
Write-Host ""
Write-Host "現在可以執行以下指令驗證 Docker context 連線：" -ForegroundColor White
Write-Host "  docker --context $ContextName ps -a" -ForegroundColor Magenta
Write-Host ""
Write-Host "在 VSCode 中整合遠端容器：" -ForegroundColor White
Write-Host "  Ctrl+Shift+P → 'Dev Containers: Attach to Running Container...'" -ForegroundColor Magenta
Write-Host "  → 點擊右上角切換 Docker Context 為 '$ContextName'" -ForegroundColor Magenta
Write-Host "  → 選擇想要進入的容器（如 login-app）" -ForegroundColor Magenta
