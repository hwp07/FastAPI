from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)

    author_id = Column(
        Integer,
        ForeignKey("authors.id"),
        nullable=False
    )

    author = relationship(
        "AuthorModel",
        back_populates="books"
    )