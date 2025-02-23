from pydantic import BaseModel
from typing import Optional
from .user import UserResponse
from datetime import datetime

class LikeCreate(BaseModel):
    like: bool

class LikeUpdate(BaseModel):
    like: bool

class LikeResponse(BaseModel): 
    id: int
    liked_by: UserResponse  
    post_id: int
    created_at:datetime

    class Config:
        from_attributes = True 