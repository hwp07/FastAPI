from model import ShipmentModel
from schemas import ShipmentCreate
from sqlalchemy.orm import Session

def register(ship: ShipmentCreate, db: Session):
    check = db.query(ShipmentModel).filter(ShipmentModel.tracking_number == ship.tracking_number).first()

    if check is not None:
            return 1
    
    new_shipment = ShipmentModel(tracking_number = ship.tracking_number)

    db.add(new_shipment)
    db.commit()
    db.refresh(new_shipment)

    return new_shipment
    
def show(db: Session):
    return db.query(ShipmentModel).all()