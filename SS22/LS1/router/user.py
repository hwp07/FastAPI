from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy.orm import Session

from SS22.LS1.services.service import RegisterUser
from SS22.LS1.schemas.schemas import RegisterRequest
from SS22.LS1.database import get_db

router = APIRouter(
    prefix="/user",
    tags=["authentication"]
)

@router.post("register")
def register(schema: RegisterRequest, db: Session = Depends(get_db)):
    new_user = RegisterUser(
        request=schema,
        db=db
    )

    return new_user