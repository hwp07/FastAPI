from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeListResponse,
    EmployeeCreateResponse,
)
from app.services.employee import get_employees, create_employee

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("", response_model=EmployeeListResponse, status_code=status.HTTP_200_OK)
def get_employee_list(db: Session = Depends(get_db)):
    employees = get_employees(db)

    return {
        "statusCode": 200,
        "message": "Lấy danh sách nhân viên thành công!",
        "data": employees,
        "error": None,
        "path": "/employees",
    }


@router.post(
    "", response_model=EmployeeCreateResponse, status_code=status.HTTP_201_CREATED
)
def create_new_employee(employee_data: EmployeeCreate, db: Session = Depends(get_db)):
    employee = create_employee(db, employee_data)

    return {
        "statusCode": 201,
        "message": "Thêm mới nhân viên thành công!",
        "data": employee,
        "error": None,
        "path": "/employees",
    }
