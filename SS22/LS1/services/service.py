from fastapi import HTTPException, status

from SS22.LS1.models.user import UserModel
from SS22.LS1.models.user import UserModel
from SS22.LS1.schemas.schemas import RegisterRequest
from sqlalchemy.orm import Session
from SS22.LS1.security.password import hass_password


def RegisterUser(request: RegisterRequest, db: Session):
    username_exit = db.query(UserModel).filter(request.username == UserModel.username).first()

    if username_exit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tai khoan ton tai"
        )

    hass_pwd = hass_password(request.password)

    new_user = UserModel(
        username=request.username,
        hash_password=hass_pwd
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

