from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from database import get_db
from models.order import OrderModel
from schemas.common import APIResponse
from schemas.order import OrderCreate, OrderItemResponse, OrderResponse
from services.order_service import create_order

router = APIRouter(prefix="/orders", tags=["Orders"])


def serialize_order(order: OrderModel) -> dict:
    return {
        "id": order.id,
        "order_code": order.order_code,
        "customer_name": order.customer_name,
        "total_amount": order.total_amount,
        "status": order.status,
        "created_at": order.created_at,
        "items": [
            {
                "id": item.id,
                "product_id": item.product_id,
                "product_name": item.product.name,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
            }
            for item in order.items
        ],
    }


@router.post("/", response_model=APIResponse, status_code=201)
def create_new_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
):
    try:
        order = create_order(
            db,
            payload.customer_name,
            [item.model_dump() for item in payload.items],
        )
    except ValueError as exc:
        return APIResponse(
            statusCode=400,
            error="Order validation error",
            message=str(exc),
            data=None,
        )
    except Exception as exc:
        return APIResponse(
            statusCode=500,
            error="Internal Server Error",
            message="Không thể tạo đơn hàng",
            data=str(exc),
        )

    # Nạp lại đầy đủ quan hệ để response.
    order = db.scalar(
        select(OrderModel)
        .where(OrderModel.id == order.id)
        .options(
            joinedload(OrderModel.items).joinedload(
                __import__("models.order_item", fromlist=["OrderItemModel"]).OrderItemModel.product
            )
        )
    )

    data = serialize_order(order)

    return APIResponse(
        statusCode=201,
        error=None,
        message="Tạo đơn hàng thành công",
        data=data,
    )


@router.get("/{id}", response_model=APIResponse)
def get_order_detail(
    id: int,
    db: Session = Depends(get_db),
):
    order = db.scalar(
        select(OrderModel)
        .where(OrderModel.id == id)
        .options(
            joinedload(OrderModel.items).joinedload(
                __import__("models.order_item", fromlist=["OrderItemModel"]).OrderItemModel.product
            )
        )
    )

    if order is None:
        return APIResponse(
            statusCode=404,
            error="Not Found",
            message="Đơn hàng không tồn tại",
            data=None,
        )

    return APIResponse(
        statusCode=200,
        error=None,
        message="Lấy chi tiết đơn hàng thành công",
        data=serialize_order(order),
    )
