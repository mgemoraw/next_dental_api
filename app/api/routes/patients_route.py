from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException


# from core import get_db
from core.deps import get_db
# from api.auth import user_dependency
from sqlalchemy.orm import Session
from api.schemas import PatientForm, PatientResponse, UserLogin, UserCreate
from api.models import Patient, User
from api.auth.authentication import get_current_active_user, get_current_user
from core.services import patient as p
from api.auth.utils import get_current_user
from typing import Annotated

# user_dependency = Annotated[dict, Depends(get_current_user)]
user_dependency = Annotated[dict, Depends(get_current_user)]

router = APIRouter(
    prefix="/dental/api/v1/patients",
    tags=['patient'],
)


@router.post("/create", response_model=None)
async def create_patient(patient: PatientForm, user: user_dependency, db: Session=Depends(get_db)):
    
    new_patient:Patient = await p.create_new_patient(db, patient, user="user")
    return new_patient

@router.get("/index", response_model=None)
async def get_patients(user:User = Depends(get_current_active_user), db:Session=Depends(get_db), limit:int=10):
  patients=db.query(Patient).limit(limit).all()
    
  if patients:
    return patients
  return {"patients": []}


@router.delete("/delete/{id}")
async def delete_patient(id: int, user:user_dependency, db:Session = Depends(get_db)):
   
   patient: Patient = await p.delete_patient(db, id, user)

   return patient

@router.get("/getDetail/{id}", response_model=None)
async def get_patient_info(id, user:user_dependency, db:Session=Depends(get_db)):
   patient = db.query(Patient).filter(Patient.id==id).first()

   if patient:
    return patient
   
   raise HTTPException(
      status_code=status.HTTP_204_NO_CONTENT,
      detail="Data not found",
   )