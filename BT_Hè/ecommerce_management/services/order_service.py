from datetime import datetime
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.order import OrderModel
from models.order_item import OrderItemModel
from models.product import ProductModel


def create_order(db: Session, customer_name: str, items: list[dict]):
    """Tạo đơn trong một transaction. Lỗi bất kỳ => rollback."""
    try:
        # Gộp các dòng mua trùng product_id để kiểm tra/trừ kho chính xác.
        requested = {}
        for item in items:
            pid = item["product_id"]
            requested[pid] = requested.get(pid, 0) + item["quantity"]

        products = {}

        # with_for_update() khóa row sản phẩm trong transaction,
        # tránh hai đơn đồng thời cùng trừ một lượng tồn kho.
        for product_id, quantity in requested.items():
            product = db.scalar(
                select(ProductModel)
                .where(ProductModel.id == product_id)
                .with_for_update()
            )

            if product is None:
                raise ValueError(f"Sản phẩm ID {product_id} không tồn tại.")

            if product.stock_quantity < quantity:
                raise ValueError(
                    f"Out of Stock: {product.name}, "
                    f"còn {product.stock_quantity}, cần {quantity}."
                )

            products[product_id] = product

        order = OrderModel(
            order_code=f"TEMP-{uuid4().hex[:12]}",
            customer_name=customer_name.strip(),
            total_amount=0.0,
            status="COMPLETED",
            created_at=datetime.utcnow(),
        )
        db.add(order)
        db.flush()

        order.order_code = f"ORD-{datetime.utcnow().year}-{order.id:06d}"

        total = 0.0

        for item in items:
            product = products[item["product_id"]]
            quantity = item["quantity"]
            unit_price = float(product.price)

            order_item = OrderItemModel(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=unit_price,
            )
            db.add(order_item)

            product.stock_quantity -= quantity
            total += unit_price * quantity

        order.total_amount = total

        db.commit()
        db.refresh(order)
        return order

    except Exception:
        db.rollback()
        raise
