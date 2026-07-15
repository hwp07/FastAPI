from fastapi import Depends, FastAPI
from fastapi.params import Query
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from schemas import CreateGame

from services import add_game, deletegame, filter_dev, get_all, get_game_by_id, search, sort_game, stat, update


app = FastAPI()

Base.metadata.create_all(bind=engine)

# API 1
@app.get("/")
def home():
    return {
        "message": "API is running"
    } 

# API 2
@app.get("/games")
def get_game(db: Session = Depends(get_db)):
    result = get_all(db)

    return {
        "message": "Danh sach tro choi",
        "data": result
    }

@app.get("/games/search")
def search_game(
    genre: str = Query(..., description="Nhap the loai: "), 
    db: Session = Depends(get_db)
):
    result = search(genre, db)
    return result

@app.get("/games/filter")
def filter_developer(
    developer: str = Query(..., description="Nhap ten tac gia: "),
    db: Session = Depends(get_db)
):
    result = filter_dev(developer, db)    
    return result


@app.get("/games/sort")
def sort_games(
    field: str = "price",
    order: str = "desc",
    db: Session = Depends(get_db)
):
    return sort_game(field, order, db)


@app.get("/games/stats")
def stats(db: Session = Depends(get_db)):
    result = stat(db)
    return result

@app.get("/games/{game_id}")
def get_game_detail(game_id: int, db: Session = Depends(get_db)):
    result = get_game_by_id(game_id, db)
    return result

@app.post("/games")
def post_game(requets: CreateGame, db: Session = Depends(get_db)):
    new_game = add_game(requets, db)
    return new_game

@app.put("/games/{game_id}")
def put_game(
    game_id: int,
    request: CreateGame,
    db: Session = Depends(get_db)
):
    return update(game_id, request, db)

@app.delete("/games/{game_id}")
def delete_game(game_id: int, db: Session = Depends(get_db)):
    deletegame(game_id, db)
    return {
        "message": "Xoa thanh cong"
    }

