from random import randrange
from typing import List
from fastapi import FastAPI, APIRouter
from app.database import engine
from app.routers import post, user, auth

# # Create all models of file models.py
# models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to my API"}


routers: List[APIRouter] = [auth, user, post]
for route in routers:
    app.include_router(route.router)
