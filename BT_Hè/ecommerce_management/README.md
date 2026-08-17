# Ecommerce Management

FastAPI + SQLAlchemy + MySQL backend theo đề bài.

## 1. Tạo database MySQL

```sql
CREATE DATABASE ecommerce_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

## 2. Cài package

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Cấu hình

Tạo file `.env` từ `.env.example`:

```env
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=ecommerce_db
```

## 4. Chạy

Đứng tại thư mục chứa `main.py`:

```bash
uvicorn main:app --reload
```

Swagger:

`http://127.0.0.1:8000/docs`

## 5. API

- GET `/products/`
- POST `/products/`
- PUT `/products/{id}`
- POST `/orders/`
- GET `/orders/{id}`
- DELETE `/categories/{id}`

## 6. Ví dụ tạo sản phẩm

```json
{
  "product_code": "P001",
  "name": "Laptop Dell XPS 15",
  "price": 25000000,
  "stock_quantity": 10,
  "category_id": 1
}
```

## 7. Ví dụ tạo đơn hàng

```json
{
  "customer_name": "Nguyễn Văn A",
  "items": [
    {
      "product_id": 1,
      "quantity": 1
    },
    {
      "product_id": 2,
      "quantity": 2
    }
  ]
}
```

## 8. Điểm quan trọng

POST `/orders/` thực hiện toàn bộ kiểm tra tồn kho, tạo order, tạo order_items,
trừ kho và commit trong cùng một transaction. Nếu một sản phẩm không đủ kho,
transaction được rollback nên không có sản phẩm nào bị trừ kho dở dang.

`with_for_update()` được dùng khi đọc sản phẩm trong transaction để khóa row
trong các tình huống đặt hàng đồng thời.
