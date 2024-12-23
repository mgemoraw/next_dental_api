from datetime import timedelta
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jwt.exceptions import InvalidTokenError
from typing import Annotated
from sqlalchemy.orm import Session
from api.schemas import UserLogin, Token
from api.auth.authentication import (
    authenticate_user, 
    create_access_token, 
    get_current_active_user, 
    get_current_user,
)

from api.models import User
from core import get_db
from fastapi.responses import JSONResponse

ACCESS_TOKEN_EXPIRE_MINUTES = 300

router = APIRouter(
    prefix="/dental/api/v1/employees",
    tags=["employees"],
    responses={404: {"description": "Not Found"}},
)


@router.get("/")
def greet():
    greeting = {"hello": "Greetings!"}
    return JSONResponse(content=greeting)

@router.post("/login", response_model=Token)
async def user_login(form_data: OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
    # db_user = authenticate_user(user.username, user.password, db)
    db_user = authenticate_user(form_data.username, form_data.password, db)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or passsword",
            headers={"WW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) 
    access_token = create_access_token(
        data = {"sub": db_user.username}, expires_delta=access_token_expires,
    )

    # Response content
    content = content={
        "access_token": access_token, 
        "token_type": "bearer", 
        "username": db_user.username, 
        "role": db_user.role,
        }
    
    response = JSONResponse(content=content)
    response.set_cookie(
        key="access_token", 
        value=access_token, 
        httponly=True,
        secure=False,
        samesite='Lax',
        ) 

    # return content
    return response


@router.post("/logout")
async def logout():
    response = JSONResponse(content={"message": "Successfully logged out"})
    # Set the cookie with an expired date
    response.delete_cookie(key="access_token")
    return response