from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# Model nội bộ chứa các trường nhạy cảm cần bảo vệ
class StudentInternal(BaseModel):
    id: int
    full_name: str
    email: str
    hashed_password: str
    internal_score: float


# Model chứa các thông tin công khai
class StudentPublic(BaseModel):
    id: int
    full_name: str
    email: str


# Dữ liệu giả lập đóng vai trò như Database của chúng ta
fake_students = [
    StudentInternal(
        id=1,
        full_name="Nguyen Van A",
        email="a@example.com",
        hashed_password="$2b$12$KIXsV9xyzUnSafePasswordHash",
        internal_score=87.5,
    ),
]

# API Endpoint trả thẳng dữ liệu nội bộ - NGUY HIỂM!
@app.get("/students-unsafe/{student_id}", response_model=StudentPublic)
def get_student_unsafe(student_id: int):
    for student in fake_students:
        if student.id == student_id:
            # Trả về toàn bộ object Database ban đầu
            return student
    raise HTTPException(status_code=404, detail="Không tìm thấy sinh viên")