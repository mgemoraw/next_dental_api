from pydantic import BaseModel
from datetime import datetime


class Patient(BaseModel):
    """patient model"""
    id: str = None
    pID: str = None
    first_name: str
    middle_name: str
    last_name: str
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
    created_by: str
    created_at: str
    updated_by: str
    updated_at: str


class PatientForm(BaseModel):
    pID: str = None
    first_name: str
    middle_name: str
    last_name: str
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
