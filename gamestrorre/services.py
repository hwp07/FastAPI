from fastapi import HTTPException
from models import Game
from sqlalchemy.orm import Session
from sqlalchemy import func
from schemas import CreateGame


def get_game_or_404(game_id: int, db: Session):
    game = db.query(Game).filter(Game.id == game_id).first()

    if not game:
        raise HTTPException(
            status_code=404,
            detail="Khong tim thay game"
        )

    return game

def find_games(column, keyword, db: Session):
    return (
        db.query(Game)
        .filter(column.ilike(f"%{keyword}%"))
        .all()
    )


def get_all(db: Session):
    result = db.query(Game).all()
    return result
    

def search(genre: str, db: Session):
    # result = db.query(Game).filter(Game.genre.ilike(f"%{genre}%")).all()
    result = find_games(Game.genre, genre, db)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Danh sach trong"
        )
    
    return result
    
def filter_dev(developer: str, db: Session):
    # result = db.query(Game).filter(Game.developer.ilike(f"%{developer}%")).all()
    result = find_games(Game.developer, developer, db)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Danh sach trong"
        )
    
    return result
    
def sort_game(
    field: str,
    order: str,
    db: Session
):

    if field not in ["price", "release_year"]:
        raise HTTPException(
            status_code=400,
            detail="field must be 'price' or 'release_year'"
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="order must be 'asc' or 'desc'"
        )

    column = getattr(Game, field)

    if order == "asc":
        return db.query(Game).order_by(column.asc()).all()

    return db.query(Game).order_by(column.desc()).all()


def stat(db: Session):
    result = (
        db.query(
            Game.genre,
            func.count(Game.id)
        )
        .group_by(Game.genre).label("total")
        .all()
    )

    data = []

    for item in result:
        data.append({
            "genre": item.genre,
            "total": item.total
        })
    
    return data

def get_game_by_id(game_id: int, db: Session):
    return get_game_or_404(game_id, db)

def add_game(requet: CreateGame, db: Session):
    new_game = Game(**requet.model_dump())

    db.add(new_game)
    db.commit()
    db.refresh(new_game)

    return new_game


def update(
    game_id: int,
    request: CreateGame,
    db: Session
):
    game = get_game_or_404(game_id, db)

    # game.game_name = request.game_name
    # game.developer = request.developer
    # game.genre = request.genre
    # game.price = request.price
    # game.release_year = request.release_year

    for key, value in request.model_dump().items():
        setattr(game, key, value)

    db.commit()
    db.refresh(game)

    return game


def deletegame(game_id: int, db: Session):

    game = get_game_or_404(game_id, db)

    db.delete(game)
    db.commit()