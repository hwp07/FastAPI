from pydantic import BaseModel

class Shipment(BaseModel):
    tracking_number: str
    status: str