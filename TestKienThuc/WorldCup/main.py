from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from schemas import CreateTeam
import services

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "API is running"
    }


@app.get("/teams")
def get_all(db: Session = Depends(get_db)):
    return services.get_all(db)


@app.get("/teams/search")
def search(
    name: str,
    db: Session = Depends(get_db)
):
    return services.search(name, db)


@app.get("/teams/sort")
def sort_team(
    order: str = "desc",
    db: Session = Depends(get_db)
):
    return services.sort(order, db)


@app.get("/teams/{team_id}")
def get_team_detail(
    team_id: int,
    db: Session = Depends(get_db)
):
    return services.get_by_id(team_id, db)


@app.post("/teams")
def add_team(
    request: CreateTeam,
    db: Session = Depends(get_db)
):
    return services.create(request, db)


@app.put("/teams/{team_id}")
def update_team(
    team_id: int,
    request: CreateTeam,
    db: Session = Depends(get_db)
):
    return services.update(team_id, request, db)


@app.delete("/teams/{team_id}")
def delete_team(
    team_id: int,
    db: Session = Depends(get_db)
):
    return services.delete(team_id, db)