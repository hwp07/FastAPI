from sqlalchemy import Column, Integer, String, Enum
from database import Base


class MedicalStaff(Base):
    __tablename__ = "medical_staff"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)

    role = Column(Enum("doctor", "pharmacist"), nullable=False)