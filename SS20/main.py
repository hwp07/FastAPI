from fastapi import FastAPI
from database import engine
from base import Base

import models.classroom
import models.student

app = FastAPI()

Base.metadata.create_all(bind = engine)

@app.get("/")
def home():
    return {"message":"API is running"}

