# tao bang

from database import Base
from sqlalchemy import Column, Integer,  String


class ShipmentModel(Base):
    __tablename__ = "Shipment"

    id = Column(Integer, primary_key=True)
    tracking_number = Column(String(50), unique=True, nullable=None)
    status = Column(String(50), default="PREPARING")


