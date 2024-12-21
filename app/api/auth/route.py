from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated

from api.auth.authentication import authenticate_user, create_access_token
from core.deps import bcrypt_context, user_dependency, db_dependency

# from core.database import get_db
# from auth.utils import get_token 

from api.schemas.token_schema import Token, TokenData, UserCreateRequest

from api.models.user import User, UserModel 



router = APIRouter(
    prefix="/auth",
    tags=['Auth'],
    responses={404: {"description": "Not Found"}}
)


def get_user_by_id(db: Session, id: int):
    return db.query(UserModel).filter(UserModel.id == id).first()
def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()



@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: UserCreateRequest):
    new_user = UserModel(
        username = create_user_request.username,
        hashed_password=bcrypt_context.hash(create_user_request.password),
    )
    user = get_user_by_email(db, new_user.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {user.username} already exists",
        )
    db.add(new_user),
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    token = create_access_token(user.username, user.id, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}
