from pydantic import BaseModel

class CreateBook(BaseModel):
    title: str
    author: str
    price: float
    pages: int

class Response(CreateBook):
    id: int
