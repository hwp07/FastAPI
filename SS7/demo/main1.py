# VIết API lấy toàn bộ danh sách sinh viên lớp CNTT2
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

students = [
    {"id": 1, "name": "phong", "password": 12341234},
    {"id": 2, "name": "phongg", "password": 12341234},
    {"id": 3, "name": "phonggg", "password": 12341234}
]

app = FastAPI()

class StudentPublic(BaseModel):
    id: int
    name: str

class StudentList(BaseModel):
    data: list[StudentPublic]

@app.get("/students", response_model=StudentList)
def get_student():
    return {
        "message": "Danh sách sinh viên",
        "data": students
    }


# viet api lay chi tiet 1 sinh vvien
@app.get("/students/{student_id}", response_model=StudentPublic)
def get_student_detail(student_id: int):
    for i in students:
        if student_id == i["id"]:
            return i
        
    raise HTTPException(
        status_code="404 Not Found",
        detail= "Khong tim thay sinh vien"
    )

#api theem sinh vien
class AddStudent(BaseModel):
    id: int
    name: str
    password: str

@app.post("/students", status_code=status.HTTP_201_CREATED)
def add_student(student: AddStudent):
    new_student = {
        "id": student.id,
        "name": student.name,
        "password": student.password
    }

    students.append(new_student)

"""
    200 - 299: Thanh công/thất bại
    400 - 499: Lỗi client
    >= 500: server
"""


"""
    CẤU TRÚC API RESPONSE

    5 THUỘC TÍNH CHÍNH
    
1. SUCCESS : THÔNG BÁO THÀNH CÔNG HOẶC THẤT BẠI
2. MESSAGE : THÔNG BÁO MÔ TẢ KẾT QUẢ TRẢ VỀ
3. DATA    : DỮ LIỆU CHÍNH TRẢ VỀ
4. ERROR   : CHI TIẾT BUG
5. META    : DỮ LIỆU CHÍNH KÈM THÊM PHÂN 
"""