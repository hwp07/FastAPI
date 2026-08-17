from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    category: str
    price: float
    borrow_count: int = 0
    available_quantity: int = 0

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True