"""
1. path paramater
2. query paramater
3. repuest body
4. type hints
"""

from fastapi import FastAPI
from pydantic import BaseModel

# lay du lieu trong db
students = [
    {
        "id": 1,
        "name": "Phong",
        "age": 18
    },
    {
        "id": 2,
        "name": "Phongg",
        "age": 22
    },
    {
        "id": 3,
        "name": "Phonggg",
        "age": 21
    }
]

app = FastAPI()

class Student(BaseModel):
    name: str
    age: int
    id: int

@app.get("/students")
def get_students():
    return{
        "message": "Lay sinh vien thanh cong",
        "data": students
    }

@app.get("students/{student_id}")
def get_student_detail(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return {
                "message": "Lay chi tiet sinh vien thanh cong!",
                "data": student
            }
        
    return {
        "message": "Khong tim thay sinh vien",
        "data": []
    }


# query paramater: tìm kiếm, lọc, phân trang
# lọc sinh viên có tuổi 21
# query nhiều điệu điệu: &

@app.get("/search")
def get_student_by_age(age: int, keyword: str):
    print("Giá trị tuổi: ", age)
    print("keyword cần tìm",keyword)

    result = []
    for student in students:
        if student["age"] == age and keyword.lower() in student["name"]:
            result.append(student)

    return {
        "data":result
    }


# request body
# thêm sinh viên vào lớp
@app.post("/students")
def create_student(student: Student):
    new_student = {
        "id": student.id,
        "name": student.name,
        "age": student.age
    }

    return {
        "message": "Theem sinh vien thanh cong",
        "data": new_student
    }