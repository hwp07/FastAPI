from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from base import Base

class ClassRoom(Base):
    __tablename__ = "classroom"

    id = Column(Integer, primary_key=True)
    class_code = Column(String(255), nullable=False, unique=True)
    class_name = Column(String(255), nullable=False, unique=True)
    max_students = Column(Integer, nullable=False)
    status = Column(String(10), default="active")
    
    students = relationship(
        "Student",
        back_populates="classroom"
    )