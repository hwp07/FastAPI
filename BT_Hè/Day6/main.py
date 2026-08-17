from fastapi import FastAPI, HTTPException
from schemas import CreateBook, Response

app = FastAPI()

book_db = []


@app.post("/books", response_model=Response)
def create_book(book: CreateBook):
    new_book = {
        "id": len(book_db) + 1,
        **book.model_dump()
    }

    book_db.append(new_book)

    return new_book


@app.get("/books/{id}", response_model=Response)
def show(id: int):
    for book in book_db:
        if book["id"] == id:
            return book

    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )