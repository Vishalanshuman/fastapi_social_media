from sqlalchemy.ext.declarative import declarative_base
from fastapi import HTTPException
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config.settings import Config

engine = create_engine(Config.DB_URL,connect_args={"check_same_thread":False})
session = sessionmaker(autoflush=False,autocommit=False,bind=engine)


Base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()