from pydantic import BaseModel, EmailStr, Field
from typing import Literal
from schemas.classroom import ClassroomResponse



class StudentCreate(BaseModel):
    student_code: str = Field(..., min_length=3, max_length=20)
    full_name: str = Field(..., min_length=2, max_length=20)
    email: EmailStr
    age: int = Field(..., gt=0, lt=60)
    gender: Literal["male", "female", "other"]
    class_id: int = Field(..., ge=1)

class EmployeeCreate(BaseModel):
    employee_code: str = Field(...,min_length=3,max_length=20)
    full_name: str = Field(...,min_length=2,max_length=100)
    email: EmailStr
    department_id: int = Field(...,ge=1)

class StudentResponse(BaseModel):
    student_code: str
    full_name: str
    email: str
    age: int
    gender: str
    classroom: ClassroomResponse