from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from SS10.demoEL.database import get_db, Base, engine
from sqlalchemy import text
import SS10.demoEL.model as model
from pydantic import BaseModel
from SS10.demoEL.student_services import create_student, get_student, get_all
# import toàn bộ model trong file model


# lệnh yêu cầu sqlalchemy quét tất cả các model đã
# import và tạo bảng tương ứng nếu chưa tồn tại
Base.metadata.create_all(bind=engine)
# bind nghĩa là gắn (liên kết) với
#  một Engine hoặc Connection.
app = FastAPI()


class Studentcreate(BaseModel):
    id: int
    full_name: str
    email: str


@app.get("/")
def welcome():
    return {"message": "Welcome to Rikei Education"}


@app.get("/test-conection")
def test_conection(db: Session = Depends(get_db)):
    try:
        # thực hiện câu lệnh truy vấn đơn giản
        db.execute(text("select 1"))

        return {"status": "succes", "message": "Kết nói thành công"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kết nói thất bại .Lỗi:{str(e)}")


# python -m uvicorn main:app --reload mới chạy dc
# hàm select insert
@app.post("/students", status_code=status.HTTP_201_CREATED)
def create_student_func(student: Studentcreate, db: Session = Depends(get_db)):
    result = create_student(
        db=db, id=student.id, full_name=student.full_name, email=student.email
    )

    return {"message": "Thêm sinh viên thành công", "data": result}


@app.get("/students/{student_id}", status_code=status.HTTP_200_OK)
def get_student_detail(student_id: int, db: Session = Depends(get_db)):
    result = get_student(db, student_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không timg thấy thông tin sinh viên",
        )

    return {"message": "Lấy thông tin thành công", "data": result}


@app.get("/students", status_code=status.HTTP_200_OK)
def get_all_student(db: Session = Depends(get_db)):
    result = get_all(db)

    return {"message": "Lấy danh sách thành công", "data": result}