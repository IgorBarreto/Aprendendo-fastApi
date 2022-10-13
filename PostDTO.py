from random import randrange
from typing import Optional
from pydantic import BaseModel


class PostDTO(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: Optional[float] = None
