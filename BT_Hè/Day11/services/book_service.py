from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from models.book_model import BookModel


def create_book(db: Session, book):
    new_book = BookModel(**book.model_dump())

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


def get_books(db: Session):
    return db.query(BookModel).all()


def get_book(db: Session, book_id: int):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book

def update_book(db: Session, book_id: int, data):
    book = get_book(db, book_id)

    for key, value in data.model_dump().items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)

    return book


def delete_book(db: Session, book_id: int):
    book = get_book(db, book_id)

    db.delete(book)
    db.commit()

    return {"message": "Deleted successfully"}

def search_books(db: Session, query: str):

    return db.query(BookModel).filter(

        or_(
            BookModel.title.ilike(f"%{query}%"),
            BookModel.author.ilike(f"%{query}%"),
            BookModel.category.ilike(f"%{query}%"))).all()

def borrow_warning(db: Session, threshold: int = 5):
    return db.query(BookModel).filter(BookModel.available_quantity <= threshold).all()

def top_borrowed(db: Session, limit: int = 5):
    return db.query(BookModel).order_by(BookModel.borrow_count.desc()).limit(limit).all()