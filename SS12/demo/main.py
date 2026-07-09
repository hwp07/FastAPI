# VIẾT API

from fastapi import FastAPI, Depends, HTTPException, status
from SS12.demo.database import SessionLocal, Base, engine
from sqlalchemy.orm import Session
from SS12.demo.models import Product
from SS12.demo.schemas import CreateProduct

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {
        "message": "API đang chạy"
    }

# Tạo hàm mở phiên làm việc với mysql
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

# Viết API lấy danh sách sản phẩm
@app.get("/products")
def get_product(db: Session = Depends(get_db)):
    product = db.query(Product).all()

    return {
        "message": "Lấy danh sách sản phẩm thành công",
        "data": product
    }

# Lấy chi tiết 1 sản phẩm
@app.get("/products/{product_id}")
def get_product_detail(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy sản phẩm"
        )
    
    return {
        "message": "Lấy chi tiết sản phẩm thành công!",
        "data": product
    }

# Viết API thêm sản phẩm
@app.post("/products")
def add_product(product: CreateProduct, db:Session = Depends(get_db)):
    new_product = Product (
        name = product.name,
        price = product.price
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "message": "Thêm sản phẩm thành công",
        "data": new_product
    }


# Viết API xóa sản phẩm
@app.delete("/products/{product_id}")
def del_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Sản phẩm không tồn tại"
        )
    
    db.delete(product)
    db.commit()
    return {
        "message": "Xóa sản phẩm thành công",
        "data": product
    }


# Viết API cập nhật
@app.put("/product/{product_id}")
def update_product(product_id: int,updateproduct: CreateProduct, db: Session = Depends(get_db)):
    product = db.query(Product).filter(product_id == CreateProduct.id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy sản phẩm"
        )
    
    product.name = updateproduct.name
    product.price = updateproduct.price

    db.commit()
    db.refresh(product)

    return {
        "message": "Update thanh cong",
        "data": product
    }