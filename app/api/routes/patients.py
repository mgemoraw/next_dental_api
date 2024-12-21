from fastapi import APIRouter, Depends

from api.schemas import patient
from core.db import fetch_patients


router = APIRouter(
    prefix="/patients",
    tags=['patients'],
)


@router.get("/", response_model=patient)
async def get_all_patients():
  patients = await fetch_patients()

  return {'data': patients }