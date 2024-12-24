from fastapi.exceptions import HTTPException
from fastapi import status, Depends, Request

from datetime import datetime, date, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from api.schemas import TokenData, UserCreate
from api.models import User
from passlib.context import CryptContext

from core.deps import bcrypt_context, user_dependency, db_dependency
from core.config import get_settings
from core.deps import SECRET_KEY, ALGORITHM, get_db

from sqlalchemy.orm import Session 

# get environment variable settings
settings = get_settings()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='api/v1/employees/login')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/employees/login')


credentials_exception = HTTPException( 
    status_code=status.HTTP_401_UNAUTHORIZED, 
    detail="Could not validate credentials", 
    headers={"WWW-Authenticate": "Bearer"}, 
    )

def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username==username).first()

    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({'exp': expire})

    # expires = datetime.now(timezone.utc) + expires_delta
    
    # return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token:str = Depends(oauth2_bearer)):
    payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
    return payload


def verify_token(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=403, detail="Token is INvalid or expired")
        return payload

    except JWTError:
        raise HTTPException(status_code=403, details="Token is invalid or expired")



import logging

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_current_active_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    
    if not token:
        logger.info(f"request client {request.cookies}")

        logger.info("Token not found in cookies")
        raise credentials_exception

    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            logger.info("Username not found in token payload")
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        logger.info("JWT Error: Invalid token")
        logger.info(f"token: {token}")
        
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    
    if user is None:
        logger.info("User not found in database")
        raise credentials_exception
    logger.info(f"User {user.username} found and authenticated")
    return user
    


def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        logger.info(f"{request.cookies}")
        logger.info("Token not found in cookies")
        raise credentials_exception

    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            logger.info("Username not found in token payload")
            raise credentials_exception
    except JWTError:
        logger.info("JWT Error: Invalid token")
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        logger.info("User not found in database")
        raise credentials_exception

    logger.info(f"User {user.username} found and authenticated")
    return user  # Return the user object
    


def get_current_user_role(token: str = Depends(oauth2_scheme)):    
    credentials_exception = HTTPException( 
        status_code=status.HTTP_401_UNAUTHORIZED,        
        detail="Could not validate credentials",        
        headers={"WWW-Authenticate": "Bearer"},
    )

    # decode jwt token and extract username   
    try:        
      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])        
      user_id: str = payload.get("sub")        
      if user_id is None:            
        raise credentials_exception    
    except JWTError:        
        raise credentials_exception    
    
    # db = SessionLocal()    
    db = get_db()
    user = db.query(User).filter(User.id == user_id).first()    
    if user is None:        
        raise credentials_exception    

    return user.role.name

def role_required(required_role: str):    
   def role_dependency(current_role: str = Depends(get_current_user_role)):        
        if current_role != required_role:            
            raise HTTPException(status_code=403, detail="Forbidden")    
        return role_dependency
