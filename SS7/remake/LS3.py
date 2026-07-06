from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

products_db = [
    {"id": 101, "name": "Bàn phím cơ", "stock": 5, "price": 1200000.0},
    {"id": 102, "name": "Chuột Gaming", "stock": 2, "price": 600000.0}
]
orders_db = []

class Product(BaseModel):
    products_id: int
    quantity: int

@app.get("/orders")
def get_order(product: Product):
    is_flag = None
    for i in products_db:
        if product.products_id == i["id"]:
            is_flag = i
            break

    if is_flag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="khong tim thay id"
        )
    
    if product.quantity < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Loi so luong"
        )
    
    if product.quantity > is_flag["stcok"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="SO luong mua lon hon so luong ton kho"
        )
    
    is_flag["stcok"] -= product.quantity
    new_order = {
        "id": len(orders_db) + 1,
        "name": is_flag['name'],
        'quantity': product.quantity,
        'price': product.quantity * is_flag["price"]
    }

    orders_db.append(new_order)
    return {
        'message': ' Them thanh cong',
        'data': new_order
    }