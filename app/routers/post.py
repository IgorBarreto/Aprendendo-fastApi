from re import search
from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app import models

from app.schemas import (
    Post as postSchema,
    PostCreate as postCreateSchema,
    User as UserSchema,
    PostOUt as postOutSchema,
)

from app.models import (
    Post as postModel,
    Vote as voteModel,
)


from app.database import engine, get_db
from app.oAuth2 import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[postOutSchema])
async def get_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):

    posts = (
        db.query(postModel, func.count(voteModel.post_id).label("votes"))
        .join(voteModel, voteModel.post_id == postModel.id, isouter=True)
        .group_by(postModel.id)
        .filter(postModel.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=postSchema)
async def create_post(
    post: postCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user),
):
    new_post = postModel(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=postOutSchema)
def get_post(id: int, db: Session = Depends(get_db)):
    post = (
        db.query(postModel, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(postModel.id == id)
        .first()
    )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    post = db.query(postModel).filter(postModel.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post does not exists",
        )
    if not (post.owner_id == current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You don't have permission",
        )
    post.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=postSchema)
def update_post(
    id: int,
    updated_post: postCreateSchema,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    post = db.query(postModel).filter(postModel.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post does not exists",
        )
    if not (post.owner_id == current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You don't have permission",
        )
    post.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post.first()
