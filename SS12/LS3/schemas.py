from pydantic import BaseModel

class ShipmentUpdate(BaseModel):
    receiver_name: str
    delivery_address: str