from fastapi import APIRouter
from models import LoggedUser


router = APIRouter()


@router.get("/")
async def greet():
    return {"hello": "Greetings"}


@router.get("/login")
async def login_user(user: LoggedUser):
    return {"user": user}
