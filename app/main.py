from typing import List
from fastapi import FastAPI, APIRouter
from app.database import engine
from app.models import Base
from app.routers import post, user, auth, vote
from pydantic import BaseSettings

# Drop tables
if False:
    Base.metadata.drop_all(bind=engine)
# Create all models of file models.py that not present in database
# Base.metadata.create_all(bind=engine)

app = FastAPI()

routers: List[APIRouter] = [auth, user, post, vote]
for route in routers:
    app.include_router(route.router)


@app.get("/")
async def root():
    return {"message": "Welcome to my API"}
