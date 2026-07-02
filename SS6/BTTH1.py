from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class CourseAdd(BaseModel):
    code: str
    name: str
    duration: int = Field(..., gt=0, description="Thời lượng phải > 0")
    fee: int = Field(..., ge=0, description="Học phí phải >= 0")


courses = [
    {"id": 1, "code": "PY101", "name": "Python Basic", "duration": 30, "fee": 3000000},
    {"id": 2, "code": "API101", "name": "FastAPI Basic", "duration": 24, "fee": 2500000},
    {"id": 3, "code": "JV101", "name": "Java Basic", "duration": 40, "fee": 4000000}
]






# thêm khóa học
@app.post("/courses", status_code=201)
def add_course(course: CourseAdd):
    if course.name.strip() == "":
        raise HTTPException(status_code=400, detail="Name cannot be empty")

    for i in courses:
        if i["code"] == course.code:
            raise HTTPException(status_code=400, detail="Code already exists")

    new_course = {
        "id": courses[-1]["id"] + 1,
        "code": course.code,
        "name": course.name,
        "duration": course.duration,
        "fee": course.fee
    }

    courses.append(new_course)

    return {
        "message": "Them khoa hoc thanh cong",
        "data": new_course
    }

# tìm kiếm + lọc
@app.get("/courses")
def show_courses(
    keyword: str = None,
    min_fee: int = None,
    max_fee: int = None
):
    result = []

    for i in courses:
        if keyword:
            if keyword.lower() not in i["name"].lower() and keyword.lower() not in i["code"].lower():
                continue

        if min_fee is not None:
            if i["fee"] < min_fee:
                continue

        if max_fee is not None:
            if i["fee"] > max_fee:
                continue

        result.append(i)

    return {
        "message": "Danh sach khoa hoc",
        "data": result
    }

# lấy chi tiết khóa học
@app.get("/courses/{course_id}")
def show_course_detail(course_id: int):
    for i in courses:
        if i["id"] == course_id:
            return {
                "message": "Tim thay khoa hoc",
                "data": i
            }

    raise HTTPException(status_code=404, detail="Course not found")

# cập nhật khóa học
@app.put("/courses/{course_id}")
def update_course(course_id: int, course: CourseAdd):

    if course.name.strip() == "":
        raise HTTPException(status_code=400, detail="Name cannot be empty")

    for i in courses:
        if i["code"] == course.code and i["id"] != course_id:
            raise HTTPException(status_code=400, detail="Code already exists")

    for i in courses:
        if i["id"] == course_id:
            i["code"] = course.code
            i["name"] = course.name
            i["duration"] = course.duration
            i["fee"] = course.fee

            return {
                "message": "Cap nhat thanh cong",
                "data": i
            }

    raise HTTPException(status_code=404, detail="Course not found")


# xóa khóa học
@app.delete("/courses/{course_id}")
def delete_course(course_id: int):

    for i in courses:
        if i["id"] == course_id:
            courses.remove(i)

            return {
                "message": "Xoa thanh cong",
                "data": i
            }

    raise HTTPException(status_code=404, detail="Course not found")

