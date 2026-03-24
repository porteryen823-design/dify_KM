# 🚀 Local PowerShell Deploy Script for AWS EC2
# 整理人：Antigravity AI & Porter

$PEM_PATH = "C:\Users\porte\Downloads\dify_ubuntu2.pem"
$LOCAL_APP_PATH = "c:\VSCode_Proj\Dify\login-app"
$EC2_IP = "52.196.249.194"
$EC2_USER = "ubuntu"
$REMOTE_PATH = "~/apps/"

Write-Host "=== 🚀 開始本地直接部署至 AWS ($EC2_IP) ===" -ForegroundColor Cyan

# 1. 建立遠端目錄
Write-Host "--- [1/3] 建立遠端目錄 ---" -ForegroundColor Yellow
ssh -i $PEM_PATH -o StrictHostKeyChecking=no "$EC2_USER@$EC2_IP" "mkdir -p $REMOTE_PATH"

# 2. 同步檔案 (SCP)
Write-Host "--- [2/3] 同步 login-app 目錄 ---" -ForegroundColor Yellow
scp -i $PEM_PATH -o StrictHostKeyChecking=no -r "$LOCAL_APP_PATH" "$EC2_USER@$EC2_IP`:$REMOTE_PATH"

# 3. 執行遠端部署腳本
Write-Host "--- [3/3] 執行遠端部署腳本 ---" -ForegroundColor Yellow
ssh -i $PEM_PATH -o StrictHostKeyChecking=no "$EC2_USER@$EC2_IP" "bash ~/apps/login-app/deploy.sh"

Write-Host "=== ✅ 本地部署完成！ ===" -ForegroundColor Green
Write-Host "🌐 訪問網址: http://$EC2_IP:5050" -ForegroundColor Cyan
