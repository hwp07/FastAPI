from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class StudentAdd(BaseModel):
    code: str
    name: str
    email: str
    age: int = Field(..., gt=0)


students = [
    {"id": 1, "code": "SV001", "name": "Nguyen Van A", "email": "a@gmail.com", "age": 20},
    {"id": 2, "code": "SV002", "name": "Tran Thi B", "email": "b@gmail.com", "age": 22},
    {"id": 3, "code": "SV003", "name": "Le Van C", "email": "c@gmail.com", "age": 18}
]

# thêm học viên
@app.post("/students", status_code=201)
def add_student(student: StudentAdd):
    if student.name.strip() == "":
        raise HTTPException(status_code=400, detail="Name cannot be empty")

    if student.email.strip() == "":
        raise HTTPException(status_code=400, detail="Email cannot be empty")

    for i in students:
        if i["code"] == student.code:
            raise HTTPException(status_code=400, detail="Code already exists")

    new_student = {
        "id": students[-1]["id"] + 1 if students else 1,
        "code": student.code,
        "name": student.name,
        "email": student.email,
        "age": student.age
    }

    students.append(new_student)

    return {
        "message": "Them hoc vien thanh cong",
        "data": new_student
    }

# tìm kiếm + lọc
@app.get("/students")
def show_students(
    keyword: str = None,
    min_age: int = None,
    max_age: int = None
):
    result = []

    for student in students:
        if keyword:
            if (
                keyword.lower() not in student["name"].lower()
                and keyword.lower() not in student["code"].lower()
                and keyword.lower() not in student["email"].lower()
            ):
                continue

        if min_age is not None:
            if student["age"] < min_age:
                continue

        if max_age is not None:
            if student["age"] > max_age:
                continue

        result.append(student)

    return {
        "message": "Danh sach hoc vien",
        "data": result
    }


# lấy chi tiết học viên
@app.get("/students/{student_id}")
def show_student_detail(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return {
                "message": "Tim thay hoc vien",
                "data": student
            }

    raise HTTPException(status_code=404, detail="Student not found")





# cập nhật học viên
@app.put("/students/{student_id}")
def update_student(student_id: int, student: StudentAdd):
    if student.name.strip() == "":
        raise HTTPException(status_code=400, detail="Name cannot be empty")

    if student.email.strip() == "":
        raise HTTPException(status_code=400, detail="Email cannot be empty")

    for i in students:
        if i["code"] == student.code and i["id"] != student_id:
            raise HTTPException(status_code=400, detail="Code already exists")

    for i in students:
        if i["id"] == student_id:
            i["code"] = student.code
            i["name"] = student.name
            i["email"] = student.email
            i["age"] = student.age

            return {
                "message": "Cap nhat thanh cong",
                "data": i
            }

    raise HTTPException(status_code=404, detail="Student not found")


# xóa học viên
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for i in students:
        if i["id"] == student_id:
            students.remove(i)

            return {
                "message": "Xoa thanh cong",
                "data": i
            }

    raise HTTPException(status_code=404, detail="Student not found")