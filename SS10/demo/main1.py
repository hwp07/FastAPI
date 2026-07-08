from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.orm import sessionmaker,declarative_base, Session

app = FastAPI()

# địa chỉ MYSQL
DATABASE_URL = "mysql+pymysql://root:21082007@localhost:3306/fastapi"

# engine: cầu nối để kêt nối SQL
engine = create_engine(DATABASE_URL)

# SessionLocal: khở tạo phiên làm viêc với database
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base: Khai báo cơ sở
Base = declarative_base()

# class product: bản thiết kế giống trong bảng SQL
class Product(Base):
    __tablename__ = "product" #tên bảng

    # thuộc tính
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)


# tạo phiên làm việc với SQL
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    #câu lệnh lấy tất cả sản phẩm trong bảng products
    products = db.query(Product).all() # ORM
    return {
        "message": "Lấy danh sách sản phẩm thành công",
        "data": products
    }

# lấy chi tiết, thêm, sửa, xóa 
