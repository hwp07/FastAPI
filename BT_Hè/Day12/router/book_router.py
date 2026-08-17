from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.book_schema import BookCreateSchema, BookResponseSchema
from services.book_service import create_book

router = APIRouter(
    prefix="/api/v1/books",
    tags=["Books"]
)


@router.post(
    "",
    response_model=BookResponseSchema,
    status_code=status.HTTP_201_CREATED
)
def create_new_book(
    book: BookCreateSchema,
    db: Session = Depends(get_db)
):
    return create_book(db, book)