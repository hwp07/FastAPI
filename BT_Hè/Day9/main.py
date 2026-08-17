from fastapi import FastAPI
from database import Base, engine
from router import router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Library Management API"
)

app.include_router(router)

@app.get("/")
def home():
    return {
        "message": "Library Management API Running"
    }