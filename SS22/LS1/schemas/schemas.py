from pydantic import BaseModel


class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequets(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    user_id: int
    username: str

class TokenResponse(BaseModel):
    access_token: str
    type_token: str
    