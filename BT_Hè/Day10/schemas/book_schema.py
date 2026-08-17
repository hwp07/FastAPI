from pydantic import BaseModel, ConfigDict


class BookCreateSchema(BaseModel):
    title: str
    author: str
    price: float
    quantity: int


class BookUpdateSchema(BaseModel):
    title: str
    author: str
    price: float
    quantity: int


class BookResponseSchema(BookCreateSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)