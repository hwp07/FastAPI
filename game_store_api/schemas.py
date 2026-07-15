from pydantic import BaseModel, Field

class CreateGame(BaseModel):
    game_name: str = Field(..., min_length=1, max_length=255)
    developer: str = Field(..., min_length=1, max_length=255)
    genre: str = Field(..., min_length=1, max_length=255)
    price: float = Field(..., gt=0)
    release_year: int = Field(..., ge=1970)