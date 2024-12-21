from sqlalchemy import String, Integer, Column, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime
from core.database import Base


class Patient(Base):
    """patient model"""
    __tablename__ = "patients"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    PID = Column(String(30), unique=True, index=True)
    fname = Column(String(30))
    mname = Column(String(30))
    lname = Column(String(30))
    dob = Column(DateTime, default=datetime.utcnow())
    sex = Column(String(10))
    preferred_language = Column(String(100))
    occupation = Column(String(100))
    address = Column(String(255))
    phone_number = Column(String(15))
    email = Column(String(50), unique=True, index=True)
    previous_medical_condition:Mapped[str] = mapped_column(String(1024))
    emergency_contact = Column(String(100))
    sergical_history:Mapped[str] = mapped_column(String(1024))
    created_by = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_by = Column(String(50))
    updated_at = Column(DateTime, default=datetime.utcnow())

