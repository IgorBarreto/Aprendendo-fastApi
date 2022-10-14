from random import randrange
from fastapi import FastAPI, status, HTTPException, Response, Depends
from sqlalchemy.orm import Session
from typing import List


from . import models
from .schemas import Post as PostSchema, PostCreate
from .models import Post as PostModel
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to my API"}


@app.get("/posts", response_model=List[PostSchema])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(PostModel).all()
    return posts


@app.post(
    "/create-post", status_code=status.HTTP_201_CREATED, response_model=PostSchema
)
async def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = PostModel(**post.dict())
    post.dict()
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model=PostSchema)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(PostModel).filter(PostModel.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(PostModel).filter(PostModel.id == id)
    print(post)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post does not exists",
        )
    post.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=PostSchema)
def update_post(id: int, updated_post: PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post does not exists",
        )
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
