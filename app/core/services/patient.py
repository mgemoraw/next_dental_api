from api.models import Patient 
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session 
# from core.security import get_password_hash
from datetime import datetime
from core.deps import get_db 

async def create_new_patient(db, data: Patient, user):
    patient = db.query(Patient).filter(Patient.PID == data.PID).first()

    if patient:
        raise HTTPException(
            status_code=422,
            detail="Patient is already regisgtered with us.",
        )

    new_patient = Patient(
        PID = data.PID,
        fname=data.fname,
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
        created_by =  user,
        created_at = datetime.now(),
        updated_by = user,
        updated_at = datetime.now(),
    )

   
    db.add(new_patient) 
    db.commit()
    db.refresh(new_patient) 
    print(f"Adding patient {new_patient}") # Debug print db.commit() 
    print(f"Patient added successfully: {new_patient}") # Debug print return new_patient       
    return new_patient


async def delete_patient(db, id, user):
    patient = db.query(Patient).filter(Patient.id==id).first()

    if patient:
        db.delete(patient)
        db.commit()
        return patient
    else:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail = "Patient Data not Found",
    )


    