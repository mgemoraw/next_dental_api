from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session 
from fastapi import Depends, HTTPException, Request, status

from passlib.context import CryptContext
from datetime import datetime, timedelta

from api.models import User, Role
from api.schemas.user import UserCreate, TokenData, UserLogin
from core.deps import SECRET_KEY, ALGORITHM, get_db

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "dental/api/v1/employees/token")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='dental/api/v1/employees/login')
oauth2_bearer_dependency=Annotated[str, Depends(oauth2_bearer)]

# Your JWT secret and algorithm

ACCESS_TOKEN_EXPIRE_MINUTES = 30


credentials_exception = HTTPException( 
    status_code=status.HTTP_401_UNAUTHORIZED, 
    detail="Could not validate credentials", 
    headers={"WWW-Authenticate": "Bearer"}, 
    )

def get_user_by_username(db: Session, username:str):
    return db.query(User).filter(User.username==username).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id==user_id).first()

def delete_user_by_id(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id==user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return "complete"
    return "failed"

def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    # role = db.query(Role).filter(Role.name==user.role).first()
    db_user = User(
        username=user.username, 
        hashed_password=hashed_password, 
        # role=user.role, 
        email=user.email,
        role_id=1,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return "complete"

def authenticate_user(username: str, password: str, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.username==username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False

    return user



# create access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_token(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=403, detail="Token is INvalid or expired")
        return payload

    except JWTError:
        raise HTTPException(status_code=403, details="Token is invalid or expired")


def get_current_user(token: oauth2_bearer_dependency):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=403, detail="Token is Invalid or expired")
        return payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Token is invalid or expired")



user_dependency = Annotated[dict, Depends(get_current_user)]
