# flex-api

LINE Flex Message 模板管理 API。資料存放於 MySQL 的 `line_flex.flex_message_templates` 表。

## Endpoints

| Method | Path              | 說明                                      |
|--------|-------------------|-------------------------------------------|
| GET    | `/`               | healthcheck                               |
| GET    | `/flex`           | 列出所有模板 id + description             |
| GET    | `/flex/{id}`      | 取得單一模板（回傳 contents 為 JSON 物件）|
| POST   | `/flex`           | 新增或覆蓋模板（upsert）                  |
| DELETE | `/flex/{id}`      | 刪除模板                                  |

## 本機測試

```bash
# 1. 透過 dify compose 啟動（profiles: mysql）
cd ../dify/docker
docker compose --profile mysql up -d db_mysql flex_api

# 2. 驗 health
curl http://localhost:8002/

# 3. 取模板
curl http://localhost:8002/flex/all_elements_demo

# 4. 新增/覆蓋模板
curl -X POST http://localhost:8002/flex \
  -H 'Content-Type: application/json' \
  -d '{"id":"hello","description":"test","contents":{"type":"bubble","body":{"type":"box","layout":"vertical","contents":[{"type":"text","text":"hi"}]}}}'
```

## 環境變數

見 `.env.example`。Docker 模式下透過 compose 注入。

## 資料表

schema 由 `sql/init.sql` 建立：

- `id` VARCHAR(64) PK — 模板識別碼
- `description` VARCHAR(255) — 人類可讀描述
- `contents` JSON — Flex Message 的 `contents` 物件（不含 altText / to）
- `created_at`, `updated_at` TIMESTAMP
