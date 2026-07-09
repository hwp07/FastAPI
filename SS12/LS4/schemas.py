from pydantic import BaseModel

class StudentResponse(BaseModel):
    id: int
    full_name: str
    email: str
