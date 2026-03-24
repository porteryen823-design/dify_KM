---
description: 將 login-app 從本地直接同步並部署至 AWS EC2
---

1. 確認本地檔案與遠端路徑正確
2. 使用 SCP 將 login-app 目錄同步至 EC2
// turbo
scp -o StrictHostKeyChecking=no -i C:\Users\porte\Downloads\dify_ubuntu2.pem -r c:\VSCode_Proj\Dify\login-app ubuntu@52.196.249.194:~/apps/

3. 透過 SSH 執行遠端部署腳本
// turbo
ssh -i C:\Users\porte\Downloads\dify_ubuntu2.pem ubuntu@52.196.249.194 "bash ~/apps/login-app/deploy.sh"

4. 驗證服務是否正常運作
// turbo
ssh -i C:\Users\porte\Downloads\dify_ubuntu2.pem ubuntu@52.196.249.194 "docker ps | grep login-app"

---
**整理人：** Antigravity AI & Porter
