from pydantic import BaseModel

class CreateBook(BaseModel):
    code: str
    title: str
    price: int
    pages: int

