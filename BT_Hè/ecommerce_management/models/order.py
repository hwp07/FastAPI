from datetime import datetime
from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class OrderModel(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    customer_name: Mapped[str] = mapped_column(String(100), nullable=False)
    total_amount: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="PENDING")
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    items = relationship(
        "OrderItemModel",
        back_populates="order",
        cascade="all, delete-orphan",
    )
