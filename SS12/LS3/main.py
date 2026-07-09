from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from schemas import ShipmentUpdate
from shipment_service import update_shipment_service

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.put("/shipments/{shipment_id}", status_code=status.HTTP_200_OK)
def update_shipment(shipment_id: int,shipment_update: ShipmentUpdate,db: Session = Depends(get_db)):
    shipment = update_shipment_service(db,shipment_id,shipment_update)

    return {
        "message": "Shipment updated successfully",
        "data": {
            "id": shipment.id,
            "tracking_code": shipment.tracking_code,
            "receiver_name": shipment.receiver_name,
            "delivery_address": shipment.delivery_address
        }
    }