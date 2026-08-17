from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    product_code: str = Field(..., min_length=4, max_length=10)
    name: str = Field(..., min_length=2, max_length=100)
    price: float = Field(..., gt=0)
    stock_quantity: int = Field(..., ge=0)
    category_id: int = Field(..., gt=0)


class ProductUpdate(BaseModel):
    price: float | None = Field(None, gt=0)
    stock_quantity: int | None = Field(None, ge=0)


class CategoryBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_code: str
    name: str
    price: float
    stock_quantity: int
    category_id: int
    category: CategoryBrief | None = None
