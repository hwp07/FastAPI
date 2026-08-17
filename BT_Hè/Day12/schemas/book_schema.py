from pydantic import BaseModel
from schemas.author_schema import AuthorResponseSchema


class BookCreateSchema(BaseModel):
    title: str
    price: float
    author_id: int

class BookResponseSchema(BaseModel):
    id: int
    title: str
    price: float
    author_id: int

    author: AuthorResponseSchema

    class Config:
        from_attributes = True