from fastapi import APIRouter, Depends, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_db
from models.category import CategoryModel
from models.product import ProductModel
from schemas.common import APIResponse
from schemas.product import ProductCreate, ProductResponse, ProductUpdate
from services.product_service import list_products

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=APIResponse)
def get_products(
    category_id: int | None = Query(None, gt=0),
    search: str | None = None,
    db: Session = Depends(get_db),
):
    products = list_products(db, category_id, search)

    data = [
        ProductResponse.model_validate(product).model_dump()
        for product in products
    ]

    return APIResponse(
        statusCode=200,
        error=None,
        message="Lấy danh sách sản phẩm thành công",
        data=data,
    )


@router.post("/", response_model=APIResponse, status_code=201)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
):
    code = payload.product_code.strip().upper()

    category = db.get(CategoryModel, payload.category_id)
    if category is None:
        return APIResponse(
            statusCode=404,
            error="Not Found",
            message="Danh mục không tồn tại",
            data=None,
        )

    exists = db.query(ProductModel).filter(
        ProductModel.product_code == code
    ).first()

    if exists:
        return APIResponse(
            statusCode=400,
            error="Duplicate product_code",
            message="Mã sản phẩm đã tồn tại",
            data=None,
        )

    product = ProductModel(
        product_code=code,
        name=payload.name.strip(),
        price=payload.price,
        stock_quantity=payload.stock_quantity,
        category_id=payload.category_id,
    )

    db.add(product)

    try:
        db.commit()
        db.refresh(product)
    except IntegrityError:
        db.rollback()
        return APIResponse(
            statusCode=400,
            error="Database constraint error",
            message="Không thể tạo sản phẩm",
            data=None,
        )

    return APIResponse(
        statusCode=201,
        error=None,
        message="Thêm sản phẩm thành công",
        data=ProductResponse.model_validate(product).model_dump(),
    )


@router.put("/{id}", response_model=APIResponse)
def update_product(
    id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
):
    product = db.get(ProductModel, id)

    if product is None:
        return APIResponse(
            statusCode=404,
            error="Not Found",
            message="Sản phẩm không tồn tại",
            data=None,
        )

    if payload.price is not None:
        product.price = payload.price

    if payload.stock_quantity is not None:
        product.stock_quantity = payload.stock_quantity

    db.commit()
    db.refresh(product)

    return APIResponse(
        statusCode=200,
        error=None,
        message="Cập nhật sản phẩm thành công",
        data=ProductResponse.model_validate(product).model_dump(),
    )
