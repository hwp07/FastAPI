from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.book_model import BookModel
from models.author_model import AuthorModel
from schemas.book_schema import BookCreateSchema


def create_book(db: Session, book_in: BookCreateSchema):

    author = (
        db.query(AuthorModel)
        .filter(AuthorModel.id == book_in.author_id)
        .first()
    )

    if author is None:
        raise HTTPException(
            status_code=400,
            detail=f"Mã tác giả author_id = {book_in.author_id} không tồn tại trong hệ thống CSDL!"
        )

    book = BookModel(
        title=book_in.title,
        price=book_in.price,
        author_id=book_in.author_id
    )

    db.add(book)
    db.commit()
    db.refresh(book)

    return book