from sqlalchemy import String, Integer, Column, DateTime
from core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


class Employee(Base):
    __tablename__ = 'employees'
    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    fname: Mapped[str] = mapped_column(String(50))
    mname: Mapped[str] = mapped_column(String(50))
    lname: Mapped[str] = mapped_column(String(50))
    email: Mapped['str'] = mapped_column(String(100), unique=True, index=True)
    dob: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    address: Mapped[str] = mapped_column(String(255))
    zipcode: Mapped[str] = mapped_column(String(30))
    phone:Mapped[str] = mapped_column(String(15))
    employed_date: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now())
    profession_name: Mapped[str] = mapped_column(String(100))


class Doctor(Base):
    __tablename__ = "doctors"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    eid: Mapped[str] = mapped_column(String(30), unique=True)
    fname: Mapped[str] = mapped_column(String(50))
    mname: Mapped[str] = mapped_column(String(50))
    lname: Mapped[str] = mapped_column(String(50))
    email: Mapped['str'] = mapped_column(String(100), unique=True, index=True)
    phone: Mapped[str] = mapped_column(String(15))
    speciality: Mapped[str] = mapped_column(String(100), default=None)
