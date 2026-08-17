from sqlalchemy.orm import Session

from models import Book
from schemas import BookUpdate



def update_book(db: Session,book_id: int,book_in: BookUpdate):
    db_book = (db.query(Book).filter(Book.id == book_id).first())

    if db_book is None:
        return None


    update_data = book_in.model_dump(exclude_unset=True)


    for key, value in update_data.items():
        setattr(db_book,key,value)


    db.commit()
    db.refresh(db_book)
    
    return db_book





def delete_book(db: Session,book_id: int):
    db_book = (db.query(Book).filter(Book.id == book_id).first())

    if db_book is None:
        return False

    db.delete(db_book)
    db.commit()

    return True