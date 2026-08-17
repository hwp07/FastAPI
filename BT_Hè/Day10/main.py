from fastapi import FastAPI
from database import Base, engine
from routers import book_router
from raw_data import raw_data


Base.metadata.create_all(bind=engine)
raw_data()

app = FastAPI(
    title="Book Management API",
    description="API quản lý sách sử dụng FastAPI và SQLAlchemy",
    version="1.0.0"
)

app.include_router(book_router.router)


@app.get("/")
def root():
    return {"message": "Chào mừng đến với Book Management API! Truy cập /docs để xem Swagger UI."}