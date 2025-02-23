import os
import shutil
from fastapi import APIRouter, Depends, HTTPException,status,File,UploadFile
from sqlalchemy.orm import Session,joinedload
from config.database import get_db
from typing import List
from config.schemas import UserCreate, UserResponse,Login,LoginResponse,UpdateUser
from config.models import User
from config.auth import hash_password,create_access_token,get_current_user,verify_password

router = APIRouter(
    prefix="/auth",
    tags=['Authentication'],
)
UPLOAD_DIR = "uploads/profile_pics/" 
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    user_exist = db.query(User).filter(User.email == user.email).first()
    if user_exist:
        raise HTTPException(status_code=400, detail="User Already Exists!")
    
    hashed_pw = hash_password(user.password)
    user = user.dict()
    user['password']=hashed_pw
    new_user = User(
        **user
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@router.post("/login",response_model=LoginResponse)
def user_login(creds:Login,db:Session=Depends(get_db)):
    user = db.query(User).filter(User.email==creds.email).first()
    if not user or not verify_password(creds.password,user.password):
        raise HTTPException("Invalid Credentials",status_code=status.HTTP_401_UNAUTHORIZED)
    acces_token = create_access_token({'sub':str(user.id)})
    return acces_token

@router.put("/update", response_model=UserResponse)
def update_user(updated_data: UpdateUser, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    previous_user = db.query(User).filter(User.id == current_user.id).first()

    if not previous_user:
        raise HTTPException(status_code=404, detail="User not found")

    if updated_data.name:
        previous_user.name = updated_data.name
    if updated_data.email:
        previous_user.email = updated_data.email
    if updated_data.profile_pic:
        previous_user.profile_pic=updated_data.profile_pic

    db.commit()
    db.refresh(previous_user)
    return previous_user

@router.put("/update-profile-pic")
def update_profile_pic(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    profile_pic: UploadFile = File(...)
):
    file_extension = profile_pic.filename.split(".")[-1]  
    file_location = f"{UPLOAD_DIR}{current_user.id}_profile.{file_extension}"
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(profile_pic.file, buffer)
    
    previous_user = db.query(User).filter(User.id == current_user.id).first()
    previous_user.profile_pic = file_location  # Save file path in DB
    
    db.commit()
    db.refresh(previous_user)
    
    return {"message": "Profile picture updated successfully", "profile_pic": file_location}