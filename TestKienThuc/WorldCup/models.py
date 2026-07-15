from database import Base
from sqlalchemy import Column, Integer, String


class Teams(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    country_name = Column(String(255), nullable=False)
    coach_name = Column(String(255), nullable=False)
    group_name = Column(String(255), nullable=False)
    points = Column(Integer, nullable=False)