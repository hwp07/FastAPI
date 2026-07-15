from fastapi import HTTPException
from models import Game
from sqlalchemy.orm import Session


def get_all(db: Session):
    result = db.query(Game).all()

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Danh sach trong"
        )