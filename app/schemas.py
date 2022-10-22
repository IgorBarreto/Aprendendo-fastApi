from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    ...


class UserBase(BaseModel):
    email: EmailStr


class UserCreeate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(UserCreeate):
    email: EmailStr
    password: str


class Token(BaseModel):
    acess_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: User

    class Config:
        orm_mode = True


class PostOUt(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True
