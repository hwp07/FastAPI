from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class ProductModel(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=False,
        index=True,
    )

    category = relationship("CategoryModel", back_populates="products")
    order_items = relationship("OrderItemModel", back_populates="product")
