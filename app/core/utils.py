from api.models.patient import Patient
from . import get_db
from api.schemas.user import UserCreate

from sqlalchemy.orm import Session 
from fastapi import Depends

# # creates user on the database
# def create_user(user: UserCreate, session: Session= Depends(get_db)) -> LoggedUser:
#     session.add(user)
#     session.commit()
#     session.refresh(user)
#     return user

# # fetch user data by username
# def get_user_by_username(username: str, session: Session = Depends(get_db)):
#     user = session.get(User, username)
#     return user

# # fetch all patients
# def fetch_patients(db: Session):
#     db.query(Patient).all()
#     return db
