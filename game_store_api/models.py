from sqlalchemy import Column, Integer, Float, String
from database import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    game_name = Column(String(255), nullable=False)
    developer = Column(String(255), nullable=False)
    genre = Column(String(255), nullable=False)

    price = Column(Float, nullable=False)
    release_year = Column(Integer, nullable=False)