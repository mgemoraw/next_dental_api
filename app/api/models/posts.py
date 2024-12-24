from typing import Optional
from api.schemas.address import Address
from core.database import Base, engine

from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime



class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    content: Mapped[str] = mapped_column(String(1024))
    user = relationship('User', back_populates='posts')


    def __repr__(self):
        return self.content


# Base.metadata.create_all(bind=engine)
