# Viết hàm lấy dữ liệu trong DATABASE

from models import Product
from schemas import CreateProduct
from fastapi import HTTPException, status
# Lấy danh sách sản phẩm
def get_product(db):
    product = db.query(Product).all()
    return product

# Lấy chi tiết sản phẩm
def get_product_detail(product_id: int, db):
    product = db.query(Product).filter(Product.id == product_id).first()
    return product

# Thêm sản phẩm
def add_product(product:CreateProduct, db):
    new_product = Product (
        **product.model_dump()
    )

    """
    new_product = Product (
        name = product.name,
        price = product.price
    )
    """

    return new_product

# Xóa sản phẩm
def del_product(product_id: int, db):
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Sản phẩm không tồn tại"
        )
    
    db.delete(product)
    db.commit()


# Cập nhật sản phẩm
def update_product(product_id: int,updateproduct: CreateProduct, db):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy sản phẩm"
        )

    product.name = updateproduct.name
    product.price = updateproduct.price

    db.commit()
    db.refresh(product)

    return product