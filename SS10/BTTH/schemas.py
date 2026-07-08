from pydantic import BaseModel

# kiem soat du lieu dau vao nguoi dung
class ShipmentCreate(BaseModel):
    tracking_number: str

# du lieu dau ra
class SHipmentResponse(BaseModel):
    id: int
    tracking_number: str
    status: str

