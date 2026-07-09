from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from database import Base,engine,get_db
from student_service import delete_student_service

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.delete("/students/{student_id}",status_code=status.HTTP_200_OK)
def delete_student(student_id: int,db: Session = Depends(get_db)):
    student = delete_student_service(db,student_id)

    return {
        "message": "Xóa học viên thành công",
        "data": student
    }