from SS10.demoEL.database import Base
from sqlalchemy import Column, Integer, String

# thiet lap model cho students

class StudentModel(Base):
    __tablename__ = "students"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    fullname = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(100),
        unique=True,
        index=True
    )