from sqlalchemy import Integer, DateTime, String, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from core import Base
from datetime import datetime 

class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    date: Mapped[DateTime] = mapped_column(DateTime)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow())
    created_by: Mapped[str] = mapped_column(String(100))
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow())
    updated_by: Mapped[str] = mapped_column(String(100))

    def __repr__(self):
        return self.name

