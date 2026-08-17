from fastapi import FastAPI

from database import Base, engine
from models import CategoryModel, ProductModel, OrderModel, OrderItemModel
from routers.product_router import router as product_router
from routers.order_router import router as order_router
from routers.category_router import router as category_router

app = FastAPI(
    title="Ecommerce Management API",
    version="1.0.0",
    description="Backend quản lý sản phẩm, đơn hàng và tồn kho.",
)

# Tạo bảng nếu chưa tồn tại.
Base.metadata.create_all(bind=engine)

app.include_router(product_router)
app.include_router(order_router)
app.include_router(category_router)


@app.get("/", tags=["System"])
def root():
    return {
        "statusCode": 200,
        "error": None,
        "message": "Ecommerce Management API is running",
        "data": {
            "docs": "/docs"
        },
    }
