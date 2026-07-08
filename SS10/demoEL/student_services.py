# đây là tầng server còn main là tầng route
# main là phần kiểu controlerr kiểm soát, để viết logic chính
# hàm service insert
from sqlalchemy.orm import Session
from SS10.demoEL.model import StudentModel


def create_student(db: Session, id: int, full_name: str, email: str):
    new_student = StudentModel(id=id, full_name=full_name, email=email)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


# hàm service select
# id ở đây là id cần tìm kiếm ở dql
def get_student(db: Session, id: int):
    """Phương thức lấy thoong tin chi tiết từ databasse
    Args:
        db (Session): _description_
        id (int): _description_

    Returns:
        _type_: _description_
    """
    return db.query(StudentModel).filter(StudentModel.id == id).first()


# Giải thích cau lệnh truy vấn
# db.query(StudentModel):
# Khởi tạo truy vấn SELECT trên
# bảng dữ liệu Sinh viên.
# .filter( ... ):
# Thiết lập điều kiện lọc WHERE theo mã định danh
# student_id.
# .first(): Lấy bản ghi đầu tiên khớp điều kiện, hoặc trả về
# None nếu không tìm thấy.


def get_all(db: Session):
    """
    Phương thức lấy tất dinh viên từ database

    Args:
        db (Session): _description_

    Returns:
        _type_: _description_
    """
    return db.query(StudentModel).all()