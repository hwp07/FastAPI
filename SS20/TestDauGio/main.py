from fastapi import FastAPI

from app.database import Base, engine
from app.models.department import Department
from app.models.employee import Employee
from app.routers.employee import router as employee_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(employee_router)
