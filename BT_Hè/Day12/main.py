from fastapi import FastAPI
from database import Base, engine

from models.author_model import AuthorModel
from models.book_model import BookModel

from router.book_router import router as book_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management API",
    version="1.0.0"
)

app.include_router(book_router)


@app.get("/")
def root():
    return {
        "message": "Library Management API is running!"
    }