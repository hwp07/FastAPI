from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    department_code = Column(String(20), unique=True, nullable=False)
    department_name = Column(String(100), nullable=False)

    employees = relationship("Employee", back_populates="department")
