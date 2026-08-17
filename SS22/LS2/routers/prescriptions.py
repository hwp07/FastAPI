from fastapi import APIRouter, Depends, HTTPException, status

from dependencies.auth import get_current_user


router = APIRouter(
    prefix="/api/v1/prescriptions",
    tags=["Prescriptions"],
)


@router.post("")
def create_prescription(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "doctor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không đủ quyền hạn",
        )

    return {
        "message": "Tạo đơn thuốc thành công",
        "doctor": current_user["username"],
    }


@router.get("/view")
def view_prescriptions(  current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["doctor","pharmacist",]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không đủ quyền hạn",
        )

    return {
        "message": "Danh sách đơn thuốc",
        "user": current_user["username"],
        "role": current_user["role"],
        "prescriptions": [],
    }