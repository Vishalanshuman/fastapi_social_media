from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    profile_pic: Optional[str]=None
    created_at:datetime

class UserResponse(UserCreate):
    id: int

    class Config:
        from_attributes = True  

class Login(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    type: str
    access_token: str

class UpdateUser(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    profile_pic:Optional[str]=None
