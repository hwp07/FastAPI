# phân tích
# 1. /products/product_id là đường dẫn cố định, không phải biến product_id
# 2. dòng @app.get("/products/product_id") đang khai báo sai parameter
# 3. vì product_id không được đặt trong dấu {}
# 4. code đúng: /products/{product_id}

from fastapi import FastAPI

app = FastAPI()

products = [
    {"id": 1, "name": "Laptop Dell", "price": 15000000},
    {"id": 2, "name": "Chuột Logitech", "price": 350000},
    {"id": 3, "name": "Bàn phím cơ", "price": 1200000}
]

@app.get("/products/{product_id}") #đưa về đúng parameter
def get_product_detail(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product

    return {
        "message": "Không tìm thấy sản phẩm"
    }