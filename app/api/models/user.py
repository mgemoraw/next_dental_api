
from typing import Optional
from api.schemas.address import Address
from core.database import Base, engine

from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from datetime import datetime


class UserModel(Base):
    __tablename__ = "users"
    id: int = Column(Integer, primary_key=True, index=True)
    userId: str  = Column(String(100), unique=True)
    username: str  = Column(String(100), unique=True)
    first_name: str = Column(String(100))
    middle_name: str = Column(String(100))
    last_name: str = Column(String(100))
    email: str = Column(String(255), unique=True, index=True)
    password: str = Column(String(100))
    is_active: bool = Column(Boolean, default=False)
    is_verified: bool = Column(Boolean, default=False)
    verified_at: bool = Column(DateTime, nullable=True, default=None)
    verified_by: bool = Column(DateTime, nullable=True, default=None)

    registered_at: datetime = Column(DateTime, nullable=True, default=None)
    updated_at: datetime = Column(DateTime, nullable=True, onupdate=datetime.now())
    created_at: datetime = Column(DateTime, nullable=True, server_default=func.now())


class User(Base):
    __tablename__ = 'logged_users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    role = Column(String(50))
    hashed_password = Column(String(1024))

