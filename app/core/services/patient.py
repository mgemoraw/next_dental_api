from api.models import Patient 
from fastapi.exceptions import HTTPException

from core.security import get_password_hash
from datetime import datetime


async def create_patient(data: Patient , db):
    patient = db.query(Patient).filter(Patient.id == data.id).first()

    if patient:
        raise HTTPException(
            status_code=422,
            detail="Email is already regisgtered with us.",
        )

    new_patient = Patient(
        PID = data.PID,
        fname=data.first_name,
        mname = data.mname,
        lname=data.lname,
        email=data.email,
        dob=data.dob,
        sex=data.sex,
        preferred_language=data.preferred_language,
        occupation=data.occupation,
        address=data.address,
        previous_medical_condition=data.previous_medical_condition,
        sergical_history=data.sergical_history,
        emergency_contact=data.emergency_contact,
        created_by = data.created_by,
        created_at = datetime.now(),
        updated_by = data.updated_by,
        updated_at = datetime.now(),
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient

