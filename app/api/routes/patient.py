from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException


from core import get_db
from api.auth import user_dependency
from sqlalchemy.orm import Session
from api.schemas import PatientForm
from api.models import Patient

# from core.services import patient

router = APIRouter(
    prefix="/patient",
    tags=['patient'],
)


@router.post("/create")
async def create_patient(patient: Patient, user: user_dependency, db: Session=Depends(get_db)):
    db_patient = db.query(Patient).filter(Patient.id == patient.id).first()
    if db_patient:
        raise HTTPException(
            status=status.HTTP_400_BAD_REQUEST,
            detail="Patient already exists",
        )

    patient.created_by = user.username 
    patient.create_new_patient(db=db, patient=patient)
    return patient

@router.get("/patients")
async def get_patients(user: user_dependency, db:Session=Depends(get_db)):
  patients=db.query(Patient).all()
    
  if patients:
    return patients
  return {"patients": []}

