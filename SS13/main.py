from datetime import datetime
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from schemas import MenuItemCreate, MenuItemUpdate, MenuItemResponse
import services

app = FastAPI()

Base.metadata.create_all(bind=engine)

def response(
    status_code: int,
    message: str,
    error,
    data,
    path: str
):
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):

    from fastapi import HTTPException

    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=response(
                exc.status_code,
                exc.detail,
                "Not Found" if exc.status_code == 404 else "Bad Request",
                None,
                request.url.path
            )
        )

    return JSONResponse(
        status_code=500,
        content=response(
            500,
            "Internal Server Error",
            "Internal Server Error",
            None,
            request.url.path
        )
    )

@app.get("/")
def home():
    return {
        "message": "Catering Menu API"
    }

@app.post("/menu-items")
def create_menu_item(menu_item: MenuItemCreate,request: Request,db: Session = Depends(get_db)):
    item = services.create_menu_item(menu_item, db)

    return response(
        201,
        "Thêm món ăn thành công",
        None,
        MenuItemResponse.model_validate(item).model_dump(),
        request.url.path
    )

@app.get("/menu-items")
def get_all_menu_items(request: Request,db: Session = Depends(get_db)):
    items = services.get_all_menu_items(db)

    return response(
        200,
        "Lấy danh sách món ăn thành công",
        None,
        [
            MenuItemResponse.model_validate(item).model_dump()
            for item in items
        ],
        request.url.path
    )

@app.get("/menu-items/{item_id}")
def get_menu_item(item_id: int,request: Request,db: Session = Depends(get_db)):
    item = services.get_menu_item(item_id, db)

    return response(
        200,
        "Lấy thông tin món ăn thành công",
        None,
        MenuItemResponse.model_validate(item).model_dump(),
        request.url.path
    )

@app.put("/menu-items/{item_id}")
def update_menu_item(item_id: int,menu_item: MenuItemUpdate,request: Request,db: Session = Depends(get_db)):
    item = services.update_menu_item(item_id,menu_item,db)

    return response(
        200,
        "Cập nhật món ăn thành công",
        None,
        MenuItemResponse.model_validate(item).model_dump(),
        request.url.path
    )

@app.delete("/menu-items/{item_id}")
def delete_menu_item(item_id: int,request: Request,db: Session = Depends(get_db)):
    services.delete_menu_item(item_id, db)

    return response(
        200,
        "Xóa món ăn thành công",
        None,
        None,
        request.url.path
    )