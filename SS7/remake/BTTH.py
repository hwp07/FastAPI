from datetime import datetime

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

promo_codes_db = {
    "SUMMER25": {
        "code": "SUMMER25",
        "discount_rate": 0.15,
        "max_budget": 50000000,
        "is_active": True
    },
    "WELCOME50": {
        "code": "WELCOME50",
        "discount_rate": 0.50,
        "max_budget": 10000000,
        "is_active": False
    }
}

class PromoInternal(BaseModel):
    code: str
    discount_rate: float
    max_budget: int
    is_active: bool


class PromoPublic(BaseModel):
    code: str
    discount_rate: float

@app.get("/promos/{code}", response_model=PromoPublic, status_code=status.HTTP_200_OK)
def get_promo(code: str):
    if code not in promo_codes_db:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ma khong ton tai"
        )
    
    promo = promo_codes_db[code]

    if promo["is_active"] is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ma giam gia het han su dung"
        )
    
    return {
        "code": code,
        "discount_rate": promo["discount_rate"]
    }


"""
cố 3 tầng lỗi:
tầng 1: lỗi do người dùng (requestvalidate)
tầng 2: do developer tự định nghĩa ra (http)
tầng 3: do server
"""
@app.exception_handler(HTTPException)
def handle_exception(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status_code": exc.status_code,
            "data": None,
            "error": exc.detail,
            "message": exc.detail,
            "timestamp": datetime.now().isoformat(),
            "path": request.url.path
        }
    )