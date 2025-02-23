from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    DB_URL = os.getenv("DATABASE_URL", "sqlite:///database.sqlite3")
    SECRET_KEY = os.getenv("SECRET_KEY", "my_secret_key")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("EXPIRY_TIME",2400)
    DOMAIN_NAME = os.getenv("DOMAIN_NAME", "http://localhost:8000")
