from pydantic import BaseModel
from pydantic import Field

class VoteReturn(BaseModel):
    post_id: int
    user_id: int

    class Config:
        orm_mode = True


class Vote(BaseModel):
    post_id: int
    direction: int = Field(..., ge=0, le=1)
