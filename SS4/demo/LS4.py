from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()
students = []


# example,examples,json_schemas_extra
class Student(BaseModel):
    full_name: str = Field(..., min_length=3, examples=["Anh Dương", "Huy Anh"])
    email: EmailStr = Field(...)
    age: int = Field(..., examples=[20])
    course: str
    phone: str


@app.post("/students")
def create_student(student: Student):
    for s in students:
        if s["email"] == student.email:
            raise HTTPException(
                status_code=409,
                detail="Email đã tồn tại"
            )
        students.append(student.model_dump())
    # model_dump chuyển từ ob thành dictionary, để tạo mới, thêm vào danh sách hiện tại
    return {"message": "Thêm học viên thành công", "student": student}