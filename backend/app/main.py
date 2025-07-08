from fastapi import FastAPI

from app import engine
from app.models import models
from app.routes import router

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(router)
