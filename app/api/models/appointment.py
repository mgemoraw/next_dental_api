from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base

class Appointment(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True, index=True)
    patient_idfk = Column(Integer, ForeignKey('patients.id', ondelete='CASCADE'), default=None)
    appointment_date = Column(DateTime)
    appointment_type = Column(String(100))
    reason = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    updated_by = Column(String(100))

    patient = relationship('Patient', back_populates='appointment')
