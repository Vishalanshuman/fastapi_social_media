from fastapi import FastAPI, staticfiles
from config.database.db import Base, engine
from routes.users import router as user_router
from routes.posts import router as post_router
from routes.comments import router as comment_router
from routes.likes import router as like_router
import os

Base.metadata.create_all(bind=engine)

app = FastAPI()




@app.get('/')
def health_api():
    return {"Health": "Good!"}

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True) 

app.mount("/uploads", staticfiles.StaticFiles(directory=UPLOAD_DIR), name="uploads")



app.include_router(user_router)
app.include_router(post_router)
app.include_router(comment_router)
app.include_router(like_router)

