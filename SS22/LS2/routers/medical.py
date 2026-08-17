from fastapi import APIRouter, HTTPException, status

from models.medical_staff import MedicalStaff
from schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from security.password import hash_password, verify_password
from security.jwt import create_access_token


router = APIRouter(
    prefix="/api/v1/medical",
    tags=["Medical Authentication"],
)


@router.post("/register")
def register(data: RegisterRequest):
    if data.username in MedicalStaff:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tài khoản đã tồn tại",
        )

    hashed_password = hash_password(data.password)

    MedicalStaff[data.username] = {
        "username": data.username,
        "password": hashed_password,
        "role": data.role,
    }

    return {
        "message": "Đăng ký thành công",
        "username": data.username,
        "role": data.role,
    }


@router.post("/login",response_model=TokenResponse)
def login(data: LoginRequest):
    user = MedicalStaff.get(data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Thông tin đăng nhập không chính xác",
        )

    password_valid = verify_password(
        data.password,
        user["password"],
    )

    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Thông tin đăng nhập không chính xác",
        )

    token = create_access_token(
        username=user["username"],
        role=user["role"],
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }