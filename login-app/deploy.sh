#!/bin/bash
# EC2 首次部署腳本 - 在 EC2 上執行一次
# 使用方式：bash ~/apps/login-app/deploy.sh

set -e

cd ~/apps/login-app

echo "=== [1/4] 確認目錄結構 ==="
ls -la
mkdir -p data

echo "=== [2/4] Build Docker Image ==="
docker build -t login-app:latest .

echo "=== [3/4] 停止並移除舊容器（若存在） ==="
docker stop login-app 2>/dev/null || true
docker rm login-app 2>/dev/null || true

echo "=== [4/4] 啟動新容器 ==="
docker run -d \
  --name login-app \
  --restart unless-stopped \
  --network docker_default \
  -p 5050:5050 \
  -v ~/apps/login-app/data:/app/data \
  login-app:latest

echo ""
echo "✅ 部署完成！目前運行中的容器："
docker ps | grep login-app

echo ""
echo "📋 查看容器日誌："
echo "  docker logs -f login-app"
echo ""
echo "🌐 訪問位址：http://$(curl -s ifconfig.me):5050"
