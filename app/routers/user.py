from random import randrange
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from app.schemas import UserCreeate, User as UserSchema
from app.models import User as UserModel
from app.database import get_db
from app import utils
from app.oAuth2 import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserSchema)
def create_user(
    user: UserCreeate,
    db: Session = Depends(get_db),
):
    hashed_password = utils.password_hash(user.password)
    new_user = UserModel(**user.dict())
    new_user.password = hashed_password
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=UserSchema)
def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user),
):
    user = db.query(UserModel).filter(UserModel.id == id).first()
    if not user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't permission to acess this infomation",
        )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Useer does not found"
        )
    return user
