from sqlalchemy.orm import Session
from model import ShipmentModel

def get_shipment(db: Session, shipment_id: int):
    shipment = (
        db.query(ShipmentModel)
        .filter(ShipmentModel.id == shipment_id)
        .first()
    )

    return shipment