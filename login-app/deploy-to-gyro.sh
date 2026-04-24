#!/bin/bash
# 🚀 Deploy login-app to dify-aws-gyro
# Usage: bash login-app/deploy-to-gyro.sh
# SSH Host must be configured in ~/.ssh/config as 'dify-aws-gyro'

set -e

echo "🔄 開始部署到 dify-aws-gyro..."
echo ""

# Step 1: Pack
echo "[1/4] 打包程式碼（排除 data/ 和快取）..."
tar \
  --exclude='login-app/data' \
  --exclude='login-app/__pycache__' \
  --exclude='login-app/.pytest_cache' \
  --exclude='login-app/*.pyc' \
  -czf /tmp/login-app-deploy.tar.gz login-app/ 2>/dev/null

TARSIZE=$(ls -lh /tmp/login-app-deploy.tar.gz | awk '{print $5}')
echo "   ✅ 完成 ($TARSIZE)"
echo ""

# Step 2: Upload
echo "[2/4] 上傳到遠端..."
scp -o ConnectTimeout=10 /tmp/login-app-deploy.tar.gz dify-aws-gyro:/tmp/ 2>/dev/null
echo "   ✅ 完成"
echo ""

# Step 3: Extract & Restart
echo "[3/4] 遠端解壓並重啟容器..."
ssh dify-aws-gyro "
  tar xzf /tmp/login-app-deploy.tar.gz -C ~/Dify/ 2>/dev/null &&
  docker restart docker-login_app-1 >/dev/null 2>&1 &&
  sleep 2
" 2>/dev/null
echo "   ✅ 完成"
echo ""

# Step 4: Verify
echo "[4/4] 驗證容器狀態..."
STATUS=$(ssh dify-aws-gyro "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | grep login" 2>/dev/null)
if [ -n "$STATUS" ]; then
    echo "   ✅ 容器運行中"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "部署完成！"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "容器狀態："
    echo "$STATUS"
    echo ""
    echo "🌐 應用位址： http://54.250.195.137:5050"
    echo "📋 檢查日誌： ssh dify-aws-gyro \"docker logs -f docker-login_app-1\""
    echo ""
else
    echo "   ❌ 容器狀態異常"
    exit 1
fi
