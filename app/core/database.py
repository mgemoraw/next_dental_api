from typing import Annotated
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from core import get_settings 


settings = get_settings()

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=30,
    pool_size=5,
    max_overflow=0
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass


# engine = create_engine("sqlite:///./data.db")

# def get_session():
#    # if you are using sqlmodel
#     with Session(engine) as session:
#         yield session

# database dependency


# def get_db():
#     db = SessionLocal()
#     # Base.metadata.create_all(bind=engine)
#     try:
#         yield  db 
#     finally:
#         db.close()

