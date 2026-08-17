from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db 
from schemas.book_schema import *
from services import book_service

router = APIRouter(
    prefix="/api/v1/books",
    tags=["Book Controller"]
)


@router.get("/", response_model=List[BookResponseSchema], status_code=status.HTTP_200_OK)
def get_all_books(db: Session = Depends(get_db)):
    return book_service.get_all_books(db)

@router.get("/{book_id}", response_model=BookResponseSchema, status_code=status.HTTP_200_OK)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    db_book = book_service.get_book_by_id(db, book_id)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    return db_book


@router.post("/", response_model=BookResponseSchema, status_code=status.HTTP_201_CREATED)
def create_book(book_data: BookCreateSchema, db: Session = Depends(get_db)):
    return book_service.create_book(db, book_data)

@router.put("/{book_id}", response_model=BookResponseSchema, status_code=status.HTTP_200_OK)
def update_book(book_id: int, book_data: BookUpdateSchema, db: Session = Depends(get_db)):
    updated_book = book_service.update_book(db, book_id, book_data)
    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    return updated_book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    deleted_book = book_service.delete_book(db, book_id)
    if not deleted_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    return None