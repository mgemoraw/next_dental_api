from datetime import timedelta
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from core.deps import get_db
from api.models.posts import Post
from api.models.user import User
from api.schemas import Token

from api.schemas.posts import PostCreate, PostResponse
from api.schemas.user import UserCreate, UserResponse
from  sqlalchemy.orm import Session 

from .utils import (
    ACCESS_TOKEN_EXPIRE_MINUTES, 
    authenticate_user, 
    create_access_token, 
    create_user, 
    get_current_user, 
    get_user_by_username, 
    verify_token, 
    delete_user_by_id, 
    get_user_by_id,
)



router = APIRouter(
    prefix="/dental/api/v1/employees",
    tags = ["auth"],
)

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/")
def greet():
    return {"message": "greetings"}




@router.delete("/delete/{id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user_by_id (db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="Username doesn't exist")
    return delete_user_by_id(db=db, user_id=user_id)


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or passsword",
            headers={"WW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data = {"sub": user.username}, expires_delta=access_token_expires,
    )

    response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True) 

    # return {"access_token": access_token, "token_type": "bearer"}
    return response


@router.get("/verity-token/{totken}")
async def verify_user_token(token: str):
    verify_token(token=token)
    return {"message": "Token is valid"}



