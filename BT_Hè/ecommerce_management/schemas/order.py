from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class OrderItemCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=100)
    items: list[OrderItemCreate] = Field(..., min_length=1)


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    product_name: str
    quantity: int
    unit_price: float


class OrderResponse(BaseModel):
    id: int
    order_code: str
    customer_name: str
    total_amount: float
    status: str
    created_at: datetime
    items: list[OrderItemResponse]
