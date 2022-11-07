from pydantic import BaseModel
from datetime import datetime

class TodoBase(BaseModel):
    description: str
    completed: bool


class TodoReturn(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
