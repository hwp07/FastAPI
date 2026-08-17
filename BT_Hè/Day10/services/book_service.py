from sqlalchemy.orm import Session
from models.book_model import BookModel
from schemas.book_schema import BookCreateSchema, BookUpdateSchema


def get_all_books(db: Session):
    return db.query(BookModel).all()

def get_book_by_id(db: Session, book_id: int):
    return db.query(BookModel).filter(BookModel.id == book_id).first()

def create_book(db: Session, book_data: BookCreateSchema):
    db_book = BookModel(**book_data.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book_data: BookUpdateSchema):
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        return None

    update_data = book_data.model_dump()
    for key, value in update_data.items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        return None

    db.delete(db_book)
    db.commit()
    return db_book