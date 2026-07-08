from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import Base, engine, get_db

import model
import service

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/shipments/{shipment_id}")
def show_shipment(
    shipment_id: int,
    db: Session = Depends(get_db)
):

    shipment = service.get_shipment(db, shipment_id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )

    return {
        "message": "Shipment found",
        "data": {
            "id": shipment.id,
            "tracking_number": shipment.tracking_number,
            "status": shipment.status
        }
    }