from sqlalchemy import Column, Integer, String
from database import Base

class ShipmentModel(Base):
    __tablename__ = "shipments"
    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String(100))
    status = Column(String(50))