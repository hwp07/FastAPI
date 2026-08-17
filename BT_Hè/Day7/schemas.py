from pydantic import BaseModel

class CreateBook(BaseModel):
    ten_sach: str
    tac_gia: str
    nam_xuat_ban: int
    so_luong: int


class Book(CreateBook):
    id: int
