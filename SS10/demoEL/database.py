from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# cấu hình kết nối
#1. định nghĩa chuỗi kết nối (connection string)
DATABASE_URL = "mysql+pymysql://root:21082007@localhost/school_database"

# 2. khởi tạo đối tượng engine quản Connection 
engine = create_engine(DATABASE_URL)

# 3. khởi tạo Factory SessionLocal dùng để sinh ra Session
SessionLocal = sessionmaker(
    autoflush=False,
    bind=engine,
    autocommit=False
)

# khai bao base class dinh nghia cac model
Base = declarative_base()


#gennerrator function quan ly vong doi database session
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()