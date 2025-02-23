from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from config.database import get_db
from config.schemas import LikeResponse,LikeCreate,LikeUpdate
from config.models import User,Post,Like
from config.auth import get_current_user

router = APIRouter(
    prefix="/like",
    tags=['Likes'],
)


@router.post("/{post_id}",response_model=LikeResponse)
def create_like(
    post_id:int,
    data:LikeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post Not Found")
    like_exists = db.query(Like).filter(Like.post_id == post_id, Like.user_id == current_user.id,Like.like==True).first()
    if like_exists:
        raise HTTPException(status_code=400, detail="You have already liked this post")
    else:
        new_like=Like(
            post_id=post_id, 
            user_id=current_user.id,
            like = data.like   
        )
        db.add(new_like)
        db.commit()
        db.refresh(new_like)
        
        return new_like



@router.get("/{like_id}",response_model=LikeResponse)
def get_like(like_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    like = db.query(Like).filter(Post.id==like_id).first()
    if not like_id:
        raise HTTPException("Like Object Not Found",status_code=404)
    return like

@router.delete("/{like_id}", status_code=status.HTTP_200_OK)
def delete_like(like_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    like = db.query(Like).filter(Like.id == like_id).first()

    if not like:
        raise HTTPException(status_code=404, detail="Like Object Not Found")
    
    if like.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    db.delete(like)
    db.commit()

    return {"message": "Post Deleted Successfully"}

@router.put("/{like_id}", response_model=LikeResponse)
def update_post(like_id:int,data:LikeUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    like = db.query(Like).filter(Like.id == like_id).first()

    if not like:
        raise HTTPException(status_code=404, detail="Like Object not found")
    if like.user_id!=current_user.id:
        raise HTTPException(status_code=404, detail="Unauthorized!")

    if data.like:
        like.like = data.like
    db.commit()
    db.refresh(like)
    return like

