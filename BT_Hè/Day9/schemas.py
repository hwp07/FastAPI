from pydantic import BaseModel

class BookUpdate(BaseModel):
    title: str
    author: str
    price: float
    quantity: int



class BookResponse(BookUpdate):
    id: int
    title: str
    author: str
    price: float
    quantity: int

