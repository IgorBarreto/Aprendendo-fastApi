from asyncio import streams
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    ...


class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


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
