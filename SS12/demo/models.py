#  BANG THIET KE TRONG SQL
from sqlalchemy import Column, Integer, String, Float
from SS12.demo.database import Base

class Product(Base):
    __tablename__ = "Products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)

