
from typing import Optional

from pydantic import BaseModel, EmailStr
from .address import Address


class UserSchema(BaseModel):
    username: str 
    email: str

class UserResponse(BaseModel):
    id: int 
    username: str 
    email: str 
    password: str
    role: str 
  
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    email: str 
    password: str
    role: str 

    class Config:
        orm_mode = True

class CreateUserRequest(BaseModel):
    pass
 
class UserModel(BaseModel):
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
    email: str
    username: str
    password: str
    role: str


class UserRoles(BaseModel):
    id: str
    role: str


class Token(BaseModel):
    access_token: str 
    token_type: str 

class TokenData(BaseModel):
    username: str | None = None 
    password: str | None = None

class UserInDB(UserSchema):
    hashed_password: str
