from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, Float, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime
from core.database import Base, engine

role_permissions = Table(
    'role_permissions', 
    Base.metadata,    
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE')),    
    Column('permission_id', Integer, ForeignKey('permissions.id', ondelete='CASCADE'))
)



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


    # appointment_idfk = Column(Integer, ForeignKey('appointments.id', ondelete='CASCADE'))
    appointment = relationship('Appointment', back_populates='patient')
    visits = relationship("Visit", back_populates="patient")
    
    def __repr__(self):
        return self.fname


class Permission(Base):    
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, index=True)    
    name = Column(String(100), unique=True, index=True)    
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")

class Role(Base):    
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)    
    name = Column(String(100), unique=True, index=True)    
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")    
    users = relationship("User", back_populates="role")



class Visit(Base):    
    __tablename__ = "visits"
    id = Column(Integer, primary_key=True, index=True)    
    patient_id = Column(Integer, ForeignKey('patients.id', ondelete='CASCADE'))    
    doctor_id = Column(Integer, ForeignKey('doctors.id', ondelete='CASCADE'))    
    payment_id = Column(Integer, ForeignKey('payments.id', ondelete='CASCADE'))    
    patient = relationship("Patient", back_populates="visits")    
    doctor = relationship("Doctor", back_populates="visits")    
    payment = relationship("Payment", back_populates="visit")


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
    
    visits = relationship("Visit", back_populates="doctor")

class Payment(Base):    
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)    
    amount = Column(Float)    
    visit = relationship("Visit", back_populates="payment")
