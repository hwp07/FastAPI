from base import Base

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True)
    student_code = Column(String(50), nullable=False, unique=True)
    full_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)

    class_id = Column(
        Integer,
        ForeignKey("classroom.id")
    )

    classroom = relationship(
        "Classroom",
        back_populates="students"
    )
