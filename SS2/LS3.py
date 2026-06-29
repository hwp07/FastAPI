# phân tích
# 1. input: danh sách sinh viên 
# 2. ouput: danh sách sinh viên có status == active, nếu không có sinh viên nào thì hiện danh sách rỗng và thông báo k có sinh viên
# 3. điều kiện status == "active"
# 4. các bước khởi tạo
# b1: khởi tạo ứng dụng FastAPI
# b2: tạo danh sách students
# b3: khai báo endpoint
# b4: duyệt, lọc các sinh vien có status == "active"
# b5: trả về kết quả


from fastapi import FastAPI

app = FastAPI()

students = [
    {"id": 1, "name": "An", "status": "active"},
    {"id": 2, "name": "Binh", "status": "inactive"},
    {"id": 3, "name": "Cuong", "status": "active"},
    {"id": 4, "name": "Dung", "status": "pending"}
]

@app.get("/students/active")
def get_active_students():
    active_students = []

    for student in students:
        if student["status"] == "active":
            active_students.append(student)

    if len(active_students) == 0:
        return {
            "message": "Không có sinh viên đang học",
            "data": []
        }

    return {
        "message": "Danh sách sinh viên đang học",
        "data": active_students
    }
