from pydantic import BaseModel
from datetime import datetime
from src.schemas.user import UserReturn

class PostBase(BaseModel):
    title: str
    content: str
    published: bool


class PostCreate(BaseModel):
    title: str
    content: str
    published: bool


class PostReturn(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    updated_at: datetime
    owner_id: int
    owner: UserReturn

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: PostReturn
    votes: int

    class Config:
        orm_mode = True
