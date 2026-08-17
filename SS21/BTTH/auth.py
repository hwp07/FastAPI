from datetime import datetime, timedelta
import bcrypt
from jose import jwt, JWTError
from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, LoginRequest


router = APIRouter()



SECRET_KEY = "my-secret-key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


# đăng ký
@router.post("/auth/register")
def register(data: UserCreate,db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email đã tồn tại"
        )

    # gash pass 
    hashed_password = bcrypt.hashpw(
        data.password.encode("utf-8"),
        bcrypt.gensalt()
    )

    # tạo user mới
    new_user = User(
        email=data.email,
        password=hashed_password.decode("utf-8")
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Đăng ký thành công",
        "user_id": new_user.id,
        "email": new_user.email
    }



# đăng nhập
@router.post("/auth/login")
def login(data: LoginRequest,db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác"
        )

    # check pass
    password_correct = bcrypt.checkpw(
        data.password.encode("utf-8"),
        user.password.encode("utf-8")
    )

    if not password_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác"
        )

    # hạn sử dụng token
    expire = datetime.utcnow() + timedelta(minutes=30)

    # JWT payload
    payload = {
        "sub": user.email,
        "user_id": user.id,
        "exp": expire
    }

    # tạo JWT
    access_token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }




def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    try:
        # giải mã JWT
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # lấy email từ sub
        email = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token không hợp lệ"
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc đã hết hạn"
        )


    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User không tồn tại"
        )

    return user



@router.get("/users/me")
def get_me(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "email": current_user.email
    }