from database import SessionLocal
from models.book_model import BookModel

def raw_data():
    db = SessionLocal()

    if db.query(BookModel).count() == 0:
        db.add_all([
            BookModel(
                title="Lập Trình Python Cơ Bản",
                author="Nguyễn Văn An",
                price=120000,
                quantity=15
            ),
            BookModel(
                title="FastAPI Web Architecture",
                author="Trần Thị Bình",
                price=250000,
                quantity=8
            ),
            BookModel(
                title="MySQL & SQLAlchemy Masterclass",
                author="Lê Hoàng Cường",
                price=180000,
                quantity=20
            ),
        ])
        db.commit()

    db.close()