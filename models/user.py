from pydantic import BaseModel
from typing import Optional
from .address import Address

class User(BaseModel):
    id: int
    userId: str
    username: str
    first_name: str
    middle_name: str
    last_name: str
    email: str
    address: Optional['Address']
    role: Optional['UserRole']

class LoggedUser(BaseModel):
    id: int
    username: str
    password: str
    role: str


class UserRole(BaseModel):
    id: str 
    role: str



