from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import StudentModel

def delete_student_service(db: Session,student_id: int):
    student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Học viên không tồn tại trong hệ thống"
        )

    result = {
        "id": student.id,
        "full_name": student.full_name,
        "email": student.email
    }

    db.delete(student)
    db.commit()

    return result