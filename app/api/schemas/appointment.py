from pydantic import BaseModel
from typing import Optional
from datetime import datetime 

from . import Patient

class Apointment(BaseModel):
    patient: Patient
    appointment_date: datetime
    appointment_type: str
    reason: str
    created_at: datetime
    updated_at: datetime
    updated_by: str

    class Config:
        orm_mode = True
    
