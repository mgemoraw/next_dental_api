
from typing import List
from api.schemas.address import Address
from core.database import Base, engine

from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime



class UserModel(Base):
    __tablename__ = "usersmodel"
    id: int = Column(Integer, primary_key=True, index=True)
    user_id: Mapped['str']  = Column(String(100), unique=True)
    username: Mapped['str']  = Column(String(100), unique=True)
    first_name: Mapped[str] = Column(String(100))
    middle_name: Mapped[str] = Column(String(100))
    last_name: Mapped[str] = Column(String(100))
    email: Mapped[str] = Column(String(255), unique=True, index=True)
    password: Mapped[str] = Column(String(100))
    role: Mapped[str] = Column(String(30), default=None)
    is_active: Mapped[bool] = Column(Boolean, default=False)
    is_verified: Mapped[bool] = Column(Boolean, default=False)
    verified_at: Mapped[bool] = Column(DateTime, nullable=True, default=None)
    verified_by: Mapped['bool'] = Column(DateTime, nullable=True, default=None)

    registered_at: Mapped[DateTime] = Column(DateTime, nullable=True, default=None)
    updated_at: Mapped[DateTime] = Column(DateTime, nullable=True, onupdate=datetime.now())
    created_at: Mapped[DateTime] = Column(DateTime, nullable=True, server_default=func.now())

    # posts = relationship("Post", back_populates='user')

    def __repr__(self):
        return self.username


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    role = Column(String(50))
    hashed_password = Column(String(1024))

    posts = relationship("Post", back_populates='user')
    role = relationship("Role", back_populates="users")

    def __repr__(self):
        return self.username



# create the database table if they don't exist
Base.metadata.create_all(bind=engine)

