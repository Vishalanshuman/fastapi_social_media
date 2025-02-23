import os
import shutil
import random
from fastapi import APIRouter, Depends, HTTPException,status,File,UploadFile,Form
from sqlalchemy.orm import Session,joinedload
from config.database import get_db
from config.schemas import CreateComment,UpdateComment,CommentResponse
from config.models import User,Post,Comment
from typing import List
from config.auth import hash_password,create_access_token,get_current_user,verify_password

router = APIRouter(
    prefix="/comment",
    tags=['Comments'],
)


@router.post("/{post_id}",response_model=CommentResponse)
def create_post(
    post_id:int,
    data:CreateComment,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_comment=Comment(
        user_id=current_user.id,
        post_id=post_id,
        comment=data.comment
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return new_comment



@router.get("/{post_id}",response_model=CommentResponse)
def user_login(post_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    comment = db.query(Comment).filter(post_id==post_id).first()
    if not comment:
        raise HTTPException("Post Not Found",status_code=404)
    if comment.user_id!=current_user.id:
        raise HTTPException("Unauthorized",status_code=403)
    return comment

@router.delete("/{post_id}", status_code=status.HTTP_200_OK)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    comment = db.query(Comment).filter(post_id == post_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment Not Found")
    
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    db.delete(comment)
    db.commit()
    return {"message": "Comment Deleted Successfully"}

@router.put("/{post_id}", response_model=CommentResponse)
def update_post(post_id:int, updated_data:UpdateComment,db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    comment = db.query(Comment).filter(post_id == post_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Post not found")
    if comment.user_id!=current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized!")

    if updated_data.comment:
        comment.content = updated_data.comment
    db.commit()
    db.refresh(comment)
    return comment
