from fastapi import FastAPI
from config.database.db import Base, engine
from routes.users import router as user_router
from routes.posts import router as post_router
from routes.comments import router as comment_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)
app.include_router(post_router)
app.include_router(comment_router)



@app.get('/')
def health_api():
    return {"Health": "Good!"}
