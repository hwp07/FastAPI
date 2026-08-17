from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import BookUpdate, BookResponse
from services import update_book, delete_book


router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


@router.put("/{id}", response_model=BookResponse)
def update_book_api(id: int,book_in: BookUpdate,db: Session = Depends(get_db)):
    book = update_book(db,id,book_in)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Sách không tồn tại trong hệ thống"
        )

    return book


@router.delete("/{id}")
def delete_book_api(id: int,db: Session = Depends(get_db)):
    result = delete_book(db,id)

    if result is False:
        raise HTTPException(
            status_code=404,
            detail="Sách không tồn tại trong hệ thống"
        )


    return {
        "message": f"Đã xóa thành công sách ID {id}"
    }