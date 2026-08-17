from pydantic import BaseModel, EmailStr, Field

from app.schemas.department import DepartmentResponse


class EmployeeCreate(BaseModel):
    employee_code: str = Field(min_length=3, max_length=20)
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    department_id: int = Field(ge=1)


class EmployeeResponse(BaseModel):
    id: int
    employee_code: str
    full_name: str
    email: EmailStr
    department: DepartmentResponse

    class Config:
        from_attributes = True


class EmployeeListResponse(BaseModel):
    statusCode: int
    message: str
    data: list[EmployeeResponse]
    error: str | None
    path: str


class EmployeeCreateResponse(BaseModel):
    statusCode: int
    message: str
    data: EmployeeResponse | None
    error: str | None
    path: str
