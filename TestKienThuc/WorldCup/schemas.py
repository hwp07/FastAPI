from pydantic import BaseModel

class CreateTeam(BaseModel):
    country_name: str
    coach_name: str
    group_name: str
    points: int