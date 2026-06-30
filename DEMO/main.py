# bước 1: import fastapi
from fastapi import FastAPI
from pydantic import BaseModel, Field

# phạm vi cấu hình swagger
# khung cấu trúc dữ (schemas)
class StudentsSchemaRequest(BaseModel):
    #Khai báo thuộc và cung cấp example
    name: str = Field(..., json_schema_extra = {"exemple": "Nguyen van a"})
    age: int = Field(...,ge = 18, le = 100, json_schema_extra = {"exemple": 29})

class StudentSchemaReponse(BaseModel):
    id: int
    name: str
    age: int
    status: str

# 2. khung phân nhóm API (tags metadata)
Tags_metadata = [
    {
        "name": "students",
        "description": "Các API liên quan"
    }
]

# 3. Khung khởi tạo úng dụng global config
app = FastAPI(
    title = "Hệ thống quản lý sinh viên",
    description = "API này giúp quản lý ính viên",
    version = "1.0.0",
    contact = {
        "name": "Bộ phận phát triển API",
        "email": "support@rikkei.edu.vn"
    },

    openapi_tags = Tags_metadata,
    docs_url = "/api/v1/swagger-docs", #tùy biến lại đường dân sưagger
    redoc_url = "/api/v1/redoc-doc", # tùy biến lại đường dẫn redoc

)

# bước 3: định nghĩa đường dẫn gốc "/" bằng phương thức GET(HTTP method)
@app.get("/")

def get_root():
    # hàm trả về dictionary, fast api chuyển đội thành dạng JSON
    return {
        "message": "Hello Rikkei Educationn"
    }

# đinh nghĩa các routing cho API chuẩn restfull
# 1. GET - Lấy danh sách
@app.get(
    path = "/students",
    tags = ["Students"],
    summary = "Danh sach sinh vien",
    response_model = StudentSchemaReponse
)
def get_students():
    print("Danh sách sinh viên: ")

    return [
        {
            "id": 1,
            "name": "Nguyên Văn A"
        }
    ]

# 2. POST - Thêm sinh viên
@app.post("/students")
def create_students():
    print("Thêm mới sinh viên:")

    return {
        "messagge": "Thêm mới sinh viên thành công"
    }

# 3. PUT - cập nhật toàn bộ thông tin sinh viên
@app.put("/students/{student_id}")
def update_student(student_id: int):
    print(f"Cập nhật sinh viên: {student_id}")

    return {
        "message": f"Cập nhật thành công sinh viên {student_id}"
    }

# 4. PATCH - cập nhật 1 phần thông tin sinh viên
@app.patch("/students/{student_id}")
def patch_student(student_id :int):
    print(f"Đã cập nhật 1 phần dữ liệu của ính viên {student_id}")

# 5. DELETE - xóa vĩnh viên thông tin sinh viên
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    print(f"Xóa học sinh: {student_id}")
    
