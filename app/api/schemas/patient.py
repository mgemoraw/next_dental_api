from pydantic import BaseModel
from datetime import datetime


class PatientBase(BaseModel):
    """patient model"""
    PID: str = None
    fname: str
    mname:str
    lname: str
    dob: datetime 
    sex: str
    preferred_language: str
    occupation: str
    address: str
    phone_number: str
    email: str
    previous_medical_condition: str
    emergency_contact: str
    sergical_history: str
    


class PatientResponse(PatientBase):
    id: int
    created_by: str
    created_at: datetime
    updated_by: str
    updated_at: datetime

    class Config:
        orm_mode = True

    
class PatientForm(PatientBase):
    pass


class DoctorAssign(BaseModel):    
   doctor_id: int

class PaymentCreate(BaseModel):    
   amount: float