from pydantic import BaseModel
from typing import Optional
from .user import UserResponse
from .comments import CommentResponse
from typing import List
from datetime import datetime

class CreatePost(BaseModel):
    media: Optional[str]=None
    content: Optional[str]=None

class PostResponse(CreatePost):
    id: int
    author:UserResponse
    comments:List[CommentResponse]
    created_at:datetime

    class Config:
        from_attributes = True  


class UpdatePost(BaseModel):
    content: Optional[str] = None
    media: Optional[str] = None
