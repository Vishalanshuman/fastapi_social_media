import os
import shutil
import random
from fastapi import APIRouter, Depends, HTTPException,status,File,UploadFile,Form
from sqlalchemy.orm import Session,joinedload
from config.database import get_db
from config.schemas import CreatePost,UpdatePost,PostResponse
from config.models import User,Post,Comment,Like
from config.settings import Config
from typing import List
from config.auth import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=['Posts'],
)
UPLOAD_DIR = "uploads/posts/" 
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/",response_model=PostResponse)
def create_post(
    content:str=Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    media: UploadFile = File(...)
):
    file_extension = media.filename.split(".")[-1]  
    file_location = f"{UPLOAD_DIR}{current_user.id}_post_{random.randint(1,9999)}.{file_extension}"
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(media.file, buffer)
    new_post=Post(
        user_id=current_user.id,
        content=content,
        media=f"{Config.DOMAIN_NAME}/{file_location}"
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post



@router.get("/{post_id}",response_model=PostResponse)
def user_login(post_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    post = db.query(Post).filter(Post.id==post_id).first()
    if not post:
        raise HTTPException("Post Not Found",status_code=404)
    return post

@router.delete("/{post_id}", status_code=status.HTTP_200_OK)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post Not Found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    db.delete(post)
    db.commit()

    return {"message": "Post Deleted Successfully"}

@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id:int,content:str=Form(None),    media: UploadFile = File(None), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == current_user.id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id!=current_user.id:
        raise HTTPException(status_code=404, detail="Unauthorized!")

    if content:
        post.content = content
    if media:
        file_extension = media.filename.split(".")[-1]  
        file_location = f"{UPLOAD_DIR}{current_user.id}_post_{random.randint(1,9999)}.{file_extension}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(media.file, buffer)
        post.media=f"{Config.DOMAIN_NAME}/{file_location}"

    db.commit()
    db.refresh(post)
    return post


@router.get("/", response_model=List[PostResponse])
def get_all_posts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    posts = (
        db.query(Post)
        .options(
            joinedload(Post.author), 
            joinedload(Post.comments).joinedload(Comment.commented_by),
            joinedload(Post.likes).joinedload(Like.liked_by)  
        )
        .all()
    )

    return posts