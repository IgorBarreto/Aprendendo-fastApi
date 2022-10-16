from random import randrange
from typing import List
from fastapi import FastAPI, APIRouter
from app.database import engine
from app import models
from app.routers import post, user, auth


# Drop tables
if True:
    models.Base.metadata.drop_all(bind=engine)
# Create all models of file models.py that not present in database
models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to my API"}


routers: List[APIRouter] = [auth, user, post]
for route in routers:
    app.include_router(route.router)
