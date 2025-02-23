from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from config.database.db import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    profile_pic = Column(String, nullable=True)  
    created_at = Column(DateTime, default=func.now())

    posts = relationship('Post', back_populates="author", cascade="all, delete")
    comments = relationship("Comment", back_populates="commented_by", cascade="all, delete")  # ✅ Added this line


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    media = Column(String, nullable=True)  
    created_at = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    author = relationship("User", back_populates="posts")
    comments = relationship('Comment', back_populates="post", cascade="all, delete")  # ✅ Fixed back_populates reference



class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)

    commented_by = relationship("User", back_populates="comments")  # ✅ Works now
    post = relationship("Post", back_populates="comments")  # ✅ Fixed back_populates reference
