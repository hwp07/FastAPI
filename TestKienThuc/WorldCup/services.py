from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Teams


def get_all(db: Session):
    return db.query(Teams).all()


def get_by_id(team_id: int, db: Session):
    team = db.query(Teams).filter(
        Teams.id == team_id
    ).first()

    if team is None:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )

    return team


def create(request, db: Session):
    new_team = Teams(**request.model_dump())

    db.add(new_team)
    db.commit()
    db.refresh(new_team)

    return new_team


def update(team_id: int, request, db: Session):
    team = get_by_id(team_id, db)

    team.country_name = request.country_name
    team.coach_name = request.coach_name
    team.group_name = request.group_name
    team.points = request.points

    db.commit()
    db.refresh(team)

    return team


def delete(team_id: int, db: Session):
    team = get_by_id(team_id, db)

    db.delete(team)
    db.commit()

    return {
        "message": "Delete successfully"
    }


def search(name: str, db: Session):
    return db.query(Teams).filter(
        Teams.group_name.like(f"%{name}%")
    ).all()


def sort(order: str, db: Session):

    if order == "asc":
        return db.query(Teams).order_by(
            Teams.points.asc()
        ).all()

    return db.query(Teams).order_by(
        Teams.points.desc()
    ).all()