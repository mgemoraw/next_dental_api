from datetime import timedelta
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jwt.exceptions import InvalidTokenError
from typing import Annotated
from sqlalchemy.orm import Session
from api.schemas.user import CreateUserRequest


from core.database import get_db
from core.services.user import create_user_account
from core.utils import get_user_by_username, create_user
from api.schemas.user import User, LoggedUser
from api.schemas.token_schema import Token, TokenData

# from api.auth.user_authentication import (
#     Token, 
#     authenticate_user, 
#     ACCESS_TOKEN_EXPIRE_MINUTES,
#     create_access_token,
#     verify_password,
#     get_current_active_user
# )

from fastapi.responses import JSONResponse


router = APIRouter(
    prefix="/dental/api/v1/users",
    tags=["users"],
    responses={404: {"description": "Not Found"}},
)


@router.get("/")
def greet():
    greeting = {"hello": "Greetings!"}
    return JSONResponse(content=greeting)


# @router.post('', status_code=status.HTTP_201_CREATED)
# async def create_user(data: CreateUserRequest, db: Session = Depends(get_db)):
#     await create_user_account(data=data, db=db)
#     payload = {"message": "Usre account has been successfully created"} 

#     return JSONResponse(content=payload)
