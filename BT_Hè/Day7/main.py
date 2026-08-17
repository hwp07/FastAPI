from fastapi import FastAPI, HTTPException
from schemas import Book, CreateBook

app = FastAPI()

danh_sach_sach = [
    {
        "id": 1,
        "ten_sach": "Nhà Giả Kim",
        "tac_gia": "Paulo Coelho",
        "nam_xuat_ban": 1988,
        "so_luong": 5
    },
    {
        "id": 2,
        "ten_sach": "Dế Mèn Phiêu Lưu Ký",
        "tac_gia": "Tô Hoài",
        "nam_xuat_ban": 1941,
        "so_luong": 8
    },
    {
        "id": 3,
        "ten_sach": "Tuổi Trẻ Đáng Giá Bao Nhiêu",
        "tac_gia": "Rosie Nguyễn",
        "nam_xuat_ban": 2016,
        "so_luong": 6
    }
]



@app.post("/api/v1/books", response_model=Book)
def create_book(book: CreateBook):
    new_book = {
        "id": len(danh_sach_sach) + 1,
        **book.model_dump()
    }
    danh_sach_sach.append(new_book)
    return new_book


@app.get("/api/v1/books", response_model=list[Book])
def get_books():
    return danh_sach_sach


@app.get("/api/v1/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in danh_sach_sach:
        if book["id"] == book_id:
            return book

    raise HTTPException(
        status_code=404,
        detail=f"Không tìm thấy sách"
    )


@app.put("/api/v1/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: CreateBook):
    for index, book in enumerate(danh_sach_sach):
        if book["id"] == book_id:

            update = {
                "id": book_id,
                **updated_book.model_dump()
            }

            danh_sach_sach[index] = update

            return update

    raise HTTPException(
        status_code=404,
        detail=f"Không tìm thấy sách"
    )



@app.delete("/api/v1/books/{book_id}")
def delete_book(book_id: int):
    for book in danh_sach_sach:
        if book["id"] == book_id:
            danh_sach_sach.remove(book)
            return {"message": "Xóa sách thành công"}

    raise HTTPException(
        status_code=404,
        detail=f"Không tìm thấy sách"
    )