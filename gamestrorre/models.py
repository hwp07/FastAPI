from database import Base
from sqlalchemy import Column, Float, Integer, String

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    game_name = Column(String(255), nullable=False)
    developer = Column(String(255), nullable=False)
    genre = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    release_year = Column(Integer, nullable=False)