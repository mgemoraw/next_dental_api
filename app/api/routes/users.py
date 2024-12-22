from datetime import timedelta
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jwt.exceptions import InvalidTokenError
from typing import Annotated
from sqlalchemy.orm import Session
from api.schemas.user import CreateUserRequest

from api.schemas import UserSchema
from api.auth.authentication import get_logged_user

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


@router.get("/me")
async def view_user_info(current_user: UserSchema = Depends(get_logged_user)):
    return current_user


