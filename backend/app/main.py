from fastapi import FastAPI

from app import engine
from app.models import models
from app.routes import league_router, match_router, roster_router, user_router

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(league_router)
app.include_router(user_router)
app.include_router(roster_router)
app.include_router(match_router)
