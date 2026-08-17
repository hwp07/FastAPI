from sqlalchemy import Column, Integer, String

from SS22.LS1.database import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False, unique=True)
    hash_password = Column(String(255), nullable=False)