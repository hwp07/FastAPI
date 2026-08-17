from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class AuthorModel(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    bio = Column(Text)

    books = relationship(
        "BookModel",
        back_populates="author",
        cascade="all, delete"
    )