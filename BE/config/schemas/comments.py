from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .user import UserResponse  # Ensure correct import

class CreateComment(BaseModel):
    comment: str

class CommentResponse(CreateComment):
    id: int
    created_at: datetime
    commented_by: UserResponse  # ✅ Fixed typo

    model_config = {"from_attributes": True}  # ✅ Pydantic v2 compatible

class UpdateComment(BaseModel):
    comment: Optional[str] = None

