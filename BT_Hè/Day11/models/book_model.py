from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float

from database import Base


class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    borrow_count = Column(Integer, default=0)
    available_quantity = Column(Integer, default=0)