from typing import Literal

from pydantic import BaseModel


class RegisterRequest(BaseModel):
    username: str
    password: str
    role: Literal["doctor", "pharmacist"]


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str