# KẾT NỐI DATABASE

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

"""
1. create_engine: tạo engine, cánh cửa trỏ đến địa chỉ database
2. sessionmaker: phiên làm việc với database

"""

DATABASE_URL = "mysql+pymysql://root:21082007@localhost:3306/fastapi"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

Base = declarative_base()

