from fastapi import FastAPI

from app import engine
from app.models import models
from app.routes import league_router

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(league_router)
