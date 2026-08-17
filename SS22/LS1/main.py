from fastapi import FastAPI
from SS22.LS1.database import Base, engine
from SS22.LS1.router.user import router as router_user

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(router_user)
