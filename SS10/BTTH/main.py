from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session

from database import *
from model import *
from schemas import *
from UserServices import *

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post('/shipments', response_model=SHipmentResponse, status_code=status.HTTP_201_CREATED)
def add_shipment(ship: ShipmentCreate, db: Session=Depends(get_db)):
    check = register(ship, db)

    if check == 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ma da bi trung"
        )
    
    return check


@app.get("/shipments",response_model=list[SHipmentResponse] ,status_code=status.HTTP_200_OK)
def show_list(db: Session = Depends(get_db)):
    return show(db)
