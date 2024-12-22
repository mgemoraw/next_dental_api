# from sqlmodel import create_engine
from fastapi import Depends
from typing import Annotated
from pathlib import Path 
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from urllib.parse import quote_plus


# sqlite_url = "sqlite:///data.db"
# connect_args = {"check_same_thread": False}
# engine = create_engine(sqlite_url, connect_args=connect_args)

BASE_DIR = Path(__file__).resolve().parent.parent.parent



env_path= os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=env_path)

SECRET_KEY=os.getenv('SECRET_KEY')
ALGORITHM=os.getenv('ALGORITHM')



class Settings(BaseSettings):
    # token
    secret_key: str = os.getenv("SECRET_KEY")
    algorithm: str = os.getenv("ALGORITHM")
    
    # Database
    DB_USER: str = os.getenv("MYSQL_USER")
    DB_PASSWORD: str =  os.getenv("MYSQL_PASSWORD")
    DB_NAME: str = os.getenv("MYSQL_DB")
    DB_HOST: str = os.getenv("MYSQL_SERVER")
    DB_PORT: str = os.getenv('MYSQL_PORT')
    DATABASE_URL: str = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

def get_settings():
    return Settings()


"""
def get_session():
    with Session(engine) as session:
        yield session

def create_tables():
    SQLModel.metadata.create_all(engine)


SessionDep = Annotated[Session, Depends(get_session)]

"""