# 北風資料庫 (Northwind Traders v2.0) 詳細資料綱目

此版本為現代化的 Northwind 2.0 (Developer / Modern Edition)，其命名與結構針對現代資料庫設計進行了優化，全面採用 `snake_case` 並統一主鍵為 `id`。

---

## 核心資料表與欄位說明

### 1. `customers` (客戶表)
| 欄位名稱 | 說明 |
|---------|------|
| **id** | (PK) 客戶 ID |
| **company** | 公司名稱 (對應舊版的 CompanyName) |
| **last_name** | 姓氏 |
| **first_name** | 名字 |
| **email_address** | 電子郵件 |
| **job_title** | 職稱 |
| **business_phone** | 公司電話 |
| **fax_number** | 傳真 |
| **address** | 地址 |
| **city** | 城市 |
| **state_province** | 州/省 |
| **zip_postal_code** | 郵遞區號 |
| **country_region** | 國家/地區 |

### 2. `employees` (員工表)
| 欄位名稱 | 說明 |
|---------|------|
| **id** | (PK) 員工 ID |
| **last_name** | 姓氏 |
| **first_name** | 名字 |
| **email_address** | 電子郵件 |
| **job_title** | 職稱 |
| **business_phone** | 辦公室電話 |
| **address**, **city**, **state_province**, **country_region** | 地址資訊 |

### 3. `products` (產品表)
| 欄位名稱 | 說明 |
|---------|------|
| **id** | (PK) 產品 ID |
| **product_code** | 產品代碼 |
| **product_name** | 產品名稱 |
| **category** | 類別 |
| **standard_cost** | 標準成本 |
| **list_price** | 定價 |
| **reorder_level** | 再訂購點 |
| **target_level** | 目標庫存 |
| **quantity_per_unit** | 每單位數量 |
| **discontinued** | 是否停產 (0/1) |

### 4. `orders` (訂單主表)
| 欄位名稱 | 說明 |
|---------|------|
| **id** | (PK) 訂單 ID |
| **employee_id** | (FK) 負責員工 |
| **customer_id** | (FK) 下單客戶 |
| **order_date** | 訂單日期 |
| **shipped_date** | 出貨日期 |
| **shipper_id** | (FK) 運貨商 |
| **ship_name** | 收貨人 |
| **ship_address**, **ship_city**, **ship_state_province**, **ship_country_region** | 收貨地資訊 |
| **shipping_fee** | 運費 |
| **status_id** | (FK) 訂單狀態 |

### 5. `order_details` (訂單明細)
| 欄位名稱 | 說明 |
|---------|------|
| **id** | (PK) 明細 ID |
| **order_id** | (FK) 所屬訂單 |
| **product_id** | (FK) 產品 ID |
| **quantity** | 數量 |
| **unit_price** | 單價 |
| **discount** | 折扣 |
| **status_id** | (FK) 明細狀態 |

### 6. `inventory_transactions` (庫存交易)
| 欄位名稱 | 說明 |
|---------|------|
| **id** | (PK) 交易 ID |
| **transaction_type** | 交易類型 (1:進貨, 2:出庫 等) |
| **transaction_created_date** | 交易日期 |
| **product_id** | (FK) 產品 ID |
| **quantity** | 交易數量 |
| **customer_order_id** | (FK) 關聯客戶訂單 |
| **purchase_order_id** | (FK) 關聯採購單 |

### 7. `suppliers` (供應商)
- **id**, **company**, **last_name**, **first_name**, **city**, **country_region**

---

## 輔助狀態表 (狀態定義)

- **`orders_status`**: id, status_name
- **`purchase_order_status`**: id, status_name
- **`inventory_transaction_types`**: id, type_name

---

## 核心關聯 SQL 示範 (Northwind 2.0 專用)

**查詢客戶與其訂單總金額：**
```sql
SELECT c.company, SUM(od.unit_price * od.quantity) AS total_spent
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN order_details od ON o.id = od.order_id
GROUP BY c.company;
```

**查詢目前產品庫存水位 (透過庫存交易表)：**
```sql
SELECT p.product_name, SUM(it.quantity) AS current_stock
FROM products p
JOIN inventory_transactions it ON p.id = it.product_id
GROUP BY p.product_name;
```

---

*最後更新：2026-03-25 (全面補齊 v2.0 欄位清單)*

**整理人：** Antigravity AI & Porter
