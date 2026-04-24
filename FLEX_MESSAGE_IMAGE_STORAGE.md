# Flex Message 圖檔存放方案

**日期**: 2026-04-22  
**版本**: 1.0  
**狀態**: ✅ 已實施（Nginx 靜態文件容器方案）

---

## 概述

為 LINE Flex Message 需要的圖片資源建立統一存放與訪問方案。採用 **Nginx 靜態文件容器**（方案 2），通過 ngrok 對外暴露。

---

## 架構設計

```
LINE User (LINE 應用)
    │
    ▼ 請求 Flex Message
┌─────────────────────────┐
│ Dify workflow           │
│ (advanced-chat)         │
│ 返回 Flex Message JSON  │
│ (含圖片 URL)            │
└──────────┬──────────────┘
           │
           ▼ 圖片引用 URL
┌─────────────────────────────────────────────────────────┐
│ Nginx 靜態文件容器 (flex-images)                        │
│ 端口: 8003                                              │
│ 掛載目錄: ./flex-images → /usr/share/nginx/html        │
└──────────┬────────────────────────────────────────────┘
           │
           ▼ ngrok 隧道
┌──────────────────────────────────────────────────────────┐
│ ngrok 公網地址                                          │
│ https://ganglionate-enrique-reasonably.ngrok-free.dev   │
└──────────────────────────────────────────────────────────┘
```

---

## 實施細節

### 1. Docker Compose 配置

**檔案**: `docker-compose-template.yaml` 或 `docker-compose.yaml`

```yaml
images_server:
  image: nginx:alpine
  container_name: flex-images
  ports:
    - "8003:80"
  volumes:
    - ./flex-images:/usr/share/nginx/html:ro
  restart: always
```

### 2. 本地目錄結構

```
EC2 或 dify-aws-gyro/
├── docker-compose.yml
├── flex-images/                  # 圖檔目錄
│   ├── avatar.jpg
│   ├── cafe_1.jpg
│   ├── cafe_2.jpg
│   ├── cafe_3.jpg
│   ├── cafe_4.jpg
│   ├── cafe_5.jpg
│   ├── extra_1.jpg
│   ├── extra_2.jpg
│   └── extra_3.jpg
├── leave-api/
├── expense-api/
└── flex-api/
```

### 3. ngrok 配置

**公網訪問地址**:
```
https://ganglionate-enrique-reasonably.ngrok-free.dev/flex-images/
```

**啟動 ngrok**:
```bash
# 向宿主機 localhost:8003 建立隧道
ngrok http 8003
```

---

## 可用圖檔清單

| 檔名 | 完整 URL | 用途 |
|------|---------|------|
| `avatar.jpg` | `https://ganglionate-enrique-reasonably.ngrok-free.dev/flex-images/avatar.jpg` | 頭像圖 |
| `cafe_1.jpg` | `https://ganglionate-enrique-reasonably.ngrok-free.dev/flex-images/cafe_1.jpg` | 咖啡廳圖片 1 |
| `cafe_2.jpg` | `https://ganglionate-enrique-reasonably.ngrok-free.dev/flex-images/cafe_2.jpg` | 咖啡廳圖片 2 |
| `cafe_3.jpg` | `https://ganglionate-enrique-reasonably.ngrok-free.dev/flex-images/cafe_3.jpg` | 咖啡廳圖片 3 |
| `cafe_4.jpg` | `https://ganglionate-enrique-reasonably.ngrok-free.dev/flex-images/cafe_4.jpg` | 咖啡廳圖片 4 |
| `cafe_5.jpg` | `https://ganglionate-enrique-reasonably.ngrok-free.dev/flex-images/cafe_5.jpg` | 咖啡廳圖片 5 |
| `extra_1.jpg` | `https://ganglionate-enrique-reasonably.ngrok-free.dev/flex-images/extra_1.jpg` | 額外資源 1 |
| `extra_2.jpg` | `https://ganglionate-enrique-reasonably.ngrok-free.dev/flex-images/extra_2.jpg` | 額外資源 2 |
| `extra_3.jpg` | `https://ganglionate-enrique-reasonably.ngrok-free.dev/flex-images/extra_3.jpg` | 額外資源 3 |

---

## Flex Message JSON 中的使用方式

### 範例 1：單張圖片

```json
{
  "type": "box",
  "layout": "vertical",
  "contents": [
    {
      "type": "image",
      "url": "https://ganglionate-enrique-reasonably.ngrok-free.dev/flex-images/cafe_1.jpg",
      "size": "full",
      "aspectRatio": "20:13",
      "aspectMode": "cover"
    }
  ]
}
```

### 範例 2：圖片 + 文字組合

```json
{
  "type": "box",
  "layout": "vertical",
  "contents": [
    {
      "type": "image",
      "url": "https://ganglionate-enrique-reasonably.ngrok-free.dev/flex-images/avatar.jpg",
      "size": "100px",
      "aspectRatio": "1:1",
      "aspectMode": "cover"
    },
    {
      "type": "text",
      "text": "咖啡廳推薦",
      "weight": "bold",
      "size": "xl"
    }
  ]
}
```

### 範例 3：輪播卡片（多張圖片）

```json
{
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://ganglionate-enrique-reasonably.ngrok-free.dev/flex-images/cafe_1.jpg",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "店家 1"
          }
        ]
      }
    },
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://ganglionate-enrique-reasonably.ngrok-free.dev/flex-images/cafe_2.jpg",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "店家 2"
          }
        ]
      }
    }
  ]
}
```

---

## 資料庫整合

### 在 MySQL 中儲存圖片 URL

若要在 flex_message_templates 表中動態管理圖片，可更新 JSON 內容：

```sql
-- 方式 1：直接更新完整 JSON（含圖片 URL）
UPDATE flex_message_templates 
SET contents = JSON_OBJECT(
  'type', 'box',
  'layout', 'vertical',
  'contents', JSON_ARRAY(
    JSON_OBJECT(
      'type', 'image',
      'url', 'https://ganglionate-enrique-reasonably.ngrok-free.dev/flex-images/cafe_1.jpg',
      'size', 'full',
      'aspectRatio', '20:13',
      'aspectMode', 'cover'
    )
  )
)
WHERE id = 'cafe_showcase';

-- 方式 2：使用 JSON_SET 部分更新
UPDATE flex_message_templates 
SET contents = JSON_SET(
  contents,
  '$.contents[0].url',
  'https://ganglionate-enrique-reasonably.ngrok-free.dev/flex-images/cafe_2.jpg'
)
WHERE id = 'cafe_showcase';

-- 驗證
SELECT id, JSON_EXTRACT(contents, '$.contents[0].url') AS image_url 
FROM flex_message_templates 
WHERE id = 'cafe_showcase';
```

---

## 操作流程

### 新增圖檔

1. **將圖檔上傳至 EC2**：
   ```bash
   scp ./new_image.jpg ec2-user@<ec2-ip>:~/dify-aws-gyro/flex-images/
   ```

2. **驗證訪問**：
   ```bash
   curl https://ganglionate-enrique-reasonably.ngrok-free.dev/flex-images/new_image.jpg
   ```

3. **在 Flex Message JSON 中引用**：
   ```json
   {
     "type": "image",
     "url": "https://ganglionate-enrique-reasonably.ngrok-free.dev/flex-images/new_image.jpg"
   }
   ```

### 更新圖檔

1. 用同名檔覆蓋舊檔（無需改 URL）
2. 可加快取清除（如需立即更新）：
   ```bash
   # Nginx 容器不做快取，但 ngrok 可能有快取
   ngrok http 8003 --cache off
   ```

---

## 故障排除

### 問題 1：圖片無法載入（404）

**症狀**：Flex Message 中圖片顯示失敗

**檢查**：
```bash
# 1. 檢查容器是否運行
docker ps | grep flex-images

# 2. 檢查圖檔是否存在
ls -la ~/dify-aws-gyro/flex-images/

# 3. 測試本地訪問
curl http://localhost:8003/avatar.jpg

# 4. 測試 ngrok 訪問
curl https://ganglionate-enrique-reasonably.ngrok-free.dev/flex-images/avatar.jpg
```

**解決**：
- 確保圖檔在 `flex-images/` 目錄中
- 檢查檔名大小寫（URL 區分大小寫）
- 確認 ngrok 隧道仍然活躍

### 問題 2：ngrok 隧道掉線

**症狀**：ngrok 地址無法訪問

**解決**：
```bash
# 重啟 ngrok
pkill -f ngrok
ngrok http 8003

# 更新 Flex Message JSON 中的 URL（若 ngrok 地址變更）
```

### 問題 3：圖片載入緩慢

**原因**：ngrok 公網延遲

**優化**：
- 優先使用 AWS CloudFront（方案 1）
- 或在生產環境改用 AWS S3 直連

---

## 遷移路線圖

| 階段 | 方案 | 用途 |
|------|------|------|
| **目前** | Nginx + ngrok | 開發/測試 |
| **短期** | Nginx + 固定域名 | 測試環境穩定化 |
| **長期** | AWS S3 + CloudFront | 生產環境上線 |

---

## 相關文件

- [REFACTOR_FLEX_MESSAGE.md](REFACTOR_FLEX_MESSAGE.md) — Flex Message 資料庫驅動架構
- [flex-api/](flex-api/) — FastAPI Flex Message 服務
- [dify/docker/docker-compose-template.yaml](dify/docker/docker-compose-template.yaml) — Docker Compose 配置

---

## 總結

✅ **已實施**: Nginx 靜態文件容器 + ngrok 隧道  
✅ **9 個圖檔已可用**: avatar + 5 個咖啡廳 + 3 個額外資源  
✅ **支援動態引用**: 可在 MySQL 中管理圖片 URL  
✅ **易於擴展**: 新增圖檔無需改配置  

**下一步**: 根據需要，遷移至 AWS S3（生產環境推薦）
