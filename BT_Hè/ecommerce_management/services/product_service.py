from sqlalchemy import or_, select
from sqlalchemy.orm import Session, joinedload
from models.product import ProductModel


def list_products(
    db: Session,
    category_id: int | None = None,
    search: str | None = None,
):
    stmt = (
        select(ProductModel)
        .options(joinedload(ProductModel.category))
        .order_by(ProductModel.id)
    )

    if category_id is not None:
        stmt = stmt.where(ProductModel.category_id == category_id)

    if search:
        keyword = f"%{search.strip()}%"
        stmt = stmt.where(
            or_(
                ProductModel.name.like(keyword),
                ProductModel.product_code.like(keyword),
            )
        )

    return db.scalars(stmt).unique().all()
