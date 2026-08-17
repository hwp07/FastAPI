from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from database import get_db
from schemas.book_schema import BookCreate, BookUpdate, BookResponse
from services import book_service

router = APIRouter(
    prefix="/api/v1/books",
    tags=["Books"]
)


@router.post("",response_model=BookResponse,status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate,db: Session = Depends(get_db)):
    return book_service.create_book(db, book)


@router.get("",response_model=list[BookResponse])
def get_books(db: Session = Depends(get_db)):
    return book_service.get_books(db)

@router.get("/{book_id}",response_model=BookResponse)
def get_book(book_id: int,db: Session = Depends(get_db)):
    return book_service.get_book(db, book_id)


@router.put("/{book_id}",response_model=BookResponse)
def update_book(book_id: int,book: BookUpdate,db: Session = Depends(get_db)):
    return book_service.update_book(db, book_id, book)

@router.delete("/{book_id}")
def delete_book(book_id: int,db: Session = Depends(get_db)):
    return book_service.delete_book(db, book_id)

@router.get("/search",response_model=list[BookResponse])
def search_book(query: str = Query(..., description="Keyword"),db: Session = Depends(get_db)):
    return book_service.search_books(db, query)

@router.get("/borrow-warning",response_model=list[BookResponse])
def borrow_warning(
    threshold: int = Query(5,description="Available quantity threshold"),
    db: Session = Depends(get_db)
):
    return book_service.borrow_warning(db, threshold)

@router.get("/top-borrowed",response_model=list[BookResponse])
def top_borrowed(
    limit: int = Query(5,description="Top borrowed books"),
    db: Session = Depends(get_db)
):
    return book_service.top_borrowed(db, limit)