from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

from pydantic import BaseModel, EmailStr

class User(BaseModel):
    username: str
    email: str
    hashed_password: str

    class Config:
        orm_mode = True


class Address(BaseModel):
    id: int = Field(primary_key=True)
    address1: str
    address2: str
    email: str
    phone: str 

    user: Optional['User'] = Relationship(back_populates='address')


class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

 
class User(BaseModel):
    id: int
    userId: str
    username: str
    first_name: str
    middle_name: str
    last_name: str
    email: str
    address: Optional['Address'] = None
    role: Optional['UserRoles'] = None

class LoggedUser(BaseModel):
    id: int
    username: str
    password: str
    role: str


class UserRoles(BaseModel):
    id: str
    role: str


class UserInDB(User):
    hashed_password: str