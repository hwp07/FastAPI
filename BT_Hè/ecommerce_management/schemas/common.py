from typing import Any
from pydantic import BaseModel


class APIResponse(BaseModel):
    statusCode: int
    error: str | None = None
    message: str
    data: Any = None
