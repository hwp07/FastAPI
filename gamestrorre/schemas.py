from pydantic import BaseModel

class CreateGame(BaseModel):
    game_name: str
    developer: str
    genre: str
    price: float
    release_year: int