from fastapi import FastAPI
from pydantic import BaseModel

# quản lý sản phẩm
#tạo dữ liệu danh sách sản phẩm ban đầu
products=[
    {
        "id":1,
        "product_name":"iphone 11",
        "price":15000000,
        "stock":5

    },
    {
        "id":2,
        "product_name":"iphone 16",
        "price":25000000,
        "stock":5

    },
    {
        "id":3,
        "product_name":"iphone 13",
        "price":18000000,
        "stock":5

    },
]


# viet api hien thi danh sach san pham
app = FastAPI()

class Product(BaseModel):
    product_name: str
    price: int
    stock: int

@app.get("/products")
def get_products():
    return {
        "message": "Lay danh sach tat ca san pham",
        "data": products
    }

#viet api lay chi tiet 1 san pham
@app.get("/products/{product_id}")
def get_product_detail(product_id: int):
    for product in products:
        if product["id"] == product_id:    
            return {
                "message": "Thong tin san pham ",
                "data": product
            }
        
    return {
        "message": "Khong tim thay san pham",
        "data": []
    }

# viet api them san pham
@app.post("/products")
def add_product(product: Product):
    new_product = {
        "id": products[-1]["id"] + 1,
        "product_name": product.product_name,
        "price": product.price,
        "stock": product.stock
    }

    products.append(new_product)

    return {
        "message": "Them san pham thanh cong",
        "data": new_product
    }


#viet api xoa
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            products.remove(product)

            return {
                "message": "Xoa san pham thanh cong",
                "data": products
            }

    return {
        "message": "Khong tim thay san pham",
        "data": products
    }

# viet api cap nhat san pham
# 2 method PUT/PATCH
@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product):
    for i in products:
        if i["id"] == product_id:
            i["product_name"] = product.product_name
            i["price"] = product.price
            i["stock"] = product.stock

            return {
                "message": "Cap nhat san pham thanh cong",
                "data": i
            }

    return {
        "message": "Khong tim thay san pham"
    }

