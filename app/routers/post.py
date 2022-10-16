from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from app import models
from app.schemas import Post as PostSchema, PostCreate, User as UserSchema
from app.models import Post as PostModel
from app.database import engine, get_db
from app.oAuth2 import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[PostSchema])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(PostModel).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostSchema)
async def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user),
):
    new_post = PostModel(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=PostSchema)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(PostModel).filter(PostModel.id == id).first()
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
    post = db.query(PostModel).filter(PostModel.id == id).first()
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


@router.put("/{id}", response_model=PostSchema)
def update_post(
    id: int,
    updated_post: PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    post = db.query(PostModel).filter(PostModel.id == id).first()
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
