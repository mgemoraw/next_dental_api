from datetime import timedelta
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status, Response, Request
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
    role_required,
)

from api.models import User, Role
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

    # grab role
    role = db.query(Role).filter(Role.id==db_user.role_id).first()
    # Response content
    content = content={
        "access_token": access_token, 
        "token_type": "bearer", 
        "username": db_user.username, 
        "role": role.name,
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



# @router.get("/admin/dashboard")
@router.get("/admin")
async def admin_dashboard(user:User = Depends(get_current_active_user)):    
    # role: str = Depends(role_required("Admin"))
   return {"message": "Welcome to the Admin Dashboard"}

# @router.get("/dentist/patients")
@router.get("/dentist")
async def dentist_patients(user:User = Depends(get_current_active_user)):  
    # role: str = Depends(role_required("Dentist"))  
   return {"message": "Access to patient records"}


@router.post("/logout")
async def logout(user: User=Depends(get_current_active_user)):
    response = JSONResponse(content={"message": "Successfully logged out"})
    # Set the cookie with an expired date
    response.delete_cookie(key="access_token")
    
    return response
