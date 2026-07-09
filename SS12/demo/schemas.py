from pydantic import BaseModel

class CreateProduct(BaseModel):
    name: str
    price: float