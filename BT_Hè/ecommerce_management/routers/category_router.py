from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models.category import CategoryModel
from models.product import ProductModel
from schemas.common import APIResponse

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.delete("/{id}", response_model=APIResponse)
def delete_category(id: int, db: Session = Depends(get_db)):
    category = db.get(CategoryModel, id)

    if category is None:
        return APIResponse(
            statusCode=404,
            error="Not Found",
            message="Danh mục không tồn tại",
            data=None,
        )

    has_products = db.scalar(
        select(ProductModel.id)
        .where(ProductModel.category_id == id)
        .limit(1)
    )

    if has_products is not None:
        return APIResponse(
            statusCode=400,
            error="Category not empty",
            message="Không thể xóa danh mục vì vẫn còn sản phẩm",
            data=None,
        )

    db.delete(category)
    db.commit()

    return APIResponse(
        statusCode=200,
        error=None,
        message="Xóa danh mục thành công",
        data={"id": id},
    )
