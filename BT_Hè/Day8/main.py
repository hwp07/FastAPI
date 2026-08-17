from fastapi import FastAPI

from schemas import CreateBook


app = FastAPI()

books = [
    {
        "code": "PY101",
        "title": "Lập trình Python cơ bản",
        "price": 120000,
        "pages": 320
    },
    {
        "code": "JAVA201",
        "title": "Lập trình Java hướng đối tượng",
        "price": 150000,
        "pages": 450
    },
    {
        "code": "SQL301",
        "title": "Cơ sở dữ liệu và SQL thực hành",
        "price": 135000,
        "pages": 280
    },
    {
        "code": "WEB401",
        "title": "Phát triển ứng dụng Web với FastAPI",
        "price": 180000,
        "pages": 380
    },
    {
        "code": "AI501",
        "title": "Nhập môn Trí tuệ nhân tạo và Machine Learning",
        "price": 220000,
        "pages": 520
    }
]

@app.get("/books")
def show_book():
    return books

@app.post("/books")
def create_book(book: CreateBook):
    books.append(book.model_dump())
    return book