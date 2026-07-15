from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Game
from schemas import CreateGame

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "API is running"
    }


# API 7 - Search theo thể loại
@app.get("/games/search", status_code=status.HTTP_200_OK)
def search_game(
    genre: str = Query(..., description="Nhập thể loại game"),
    db: Session = Depends(get_db)
):
    result = (
        db.query(Game)
        .filter(Game.genre.ilike(f"%{genre}%"))
        .all()
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy game thuộc thể loại này."
        )

    return result


# API 8 - Filter theo nhà phát triển
@app.get("/games/filter", status_code=status.HTTP_200_OK)
def filter_developer(
    developer: str = Query(..., description="Tên nhà phát triển"),
    db: Session = Depends(get_db)
):
    result = (
        db.query(Game)
        .filter(Game.developer.ilike(f"%{developer}%"))
        .all()
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy nhà phát triển."
        )

    return result


# API 9 - Sort
@app.get("/games/sort")
def sort_games(
    field: str = "price",
    order: str = "desc",
    db: Session = Depends(get_db)
):

    if field not in ["price", "release_year"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="field must be 'price' or 'release_year'"
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="order must be 'asc' or 'desc'"
        )

    column = getattr(Game, field)

    if order == "asc":
        return db.query(Game).order_by(column.asc()).all()

    return db.query(Game).order_by(column.desc()).all()


# API 10 - Stats
@app.get("/games/stats")
def stats(db: Session = Depends(get_db)):

    result = (
        db.query(
            Game.genre,
            func.count(Game.id).label("total")
        )
        .group_by(Game.genre)
        .all()
    )

    data = []

    for item in result:
        data.append({
            "genre": item.genre,
            "total": item.total
        })

    return data


# API 2
@app.get("/games", status_code=status.HTTP_200_OK)
def get_all(db: Session = Depends(get_db)):
    return db.query(Game).all()


# API 3
@app.get("/games/{game_id}", status_code=status.HTTP_200_OK)
def get_detail(game_id: int, db: Session = Depends(get_db)):

    result = db.query(Game).filter(Game.id == game_id).first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy game."
        )

    return result


# API 4
@app.post("/games", status_code=status.HTTP_201_CREATED)
def add_game(
    request: CreateGame,
    db: Session = Depends(get_db)
):

    new_game = Game(**request.model_dump())

    db.add(new_game)
    db.commit()
    db.refresh(new_game)

    return new_game


# API 5
@app.put("/games/{game_id}", status_code=status.HTTP_200_OK)
def update_game(
    game_id: int,
    request: CreateGame,
    db: Session = Depends(get_db)
):

    result = db.query(Game).filter(Game.id == game_id).first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy game."
        )

    result.game_name = request.game_name
    result.developer = request.developer
    result.genre = request.genre
    result.price = request.price
    result.release_year = request.release_year

    db.commit()
    db.refresh(result)

    return result


# API 6
@app.delete("/games/{game_id}", status_code=status.HTTP_200_OK)
def delete_game(
    game_id: int,
    db: Session = Depends(get_db)
):

    result = db.query(Game).filter(Game.id == game_id).first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy game."
        )

    db.delete(result)
    db.commit()

    return {
        "message": "Xóa game thành công."
    }