from fastapi.exceptions import HTTPException
from fastapi import status, Depends, Request

from datetime import datetime, date, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from api.schemas import TokenData, UserSchema, UserCreate
from api.models import User
from passlib.context import CryptContext

from core.deps import bcrypt_context, user_dependency, db_dependency
from core.config import get_settings
from core.deps import SECRET_KEY, ALGORITHM, get_db

from sqlalchemy.orm import Session 

# get environment variable settings
settings = get_settings()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='api/v1/token')


credentials_exception = HTTPException( 
    status_code=status.HTTP_401_UNAUTHORIZED, 
    detail="Could not validate credentials", 
    headers={"WWW-Authenticate": "Bearer"}, 
    )

def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username==username).first()

    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})

    return jwt.encode(encode, settings.secret_key, algorithm=settings.algorithm)


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
        logger.info("Token not found in cookies")
        raise credentials_exception
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            logger.info("Username not found in token payload")
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        logger.info("JWT Error: Invalid token")
        logger.info(f"token: {token}")
        data = decode_access_token(token)
        print(data)
        raise credentials_exception
    user = db.query(User).filter(User.username == token_data.username).first()
    
    if user is None:
        logger.info("User not found in database")
        raise credentials_exception
    logger.info(f"User {user.username} found and authenticated")
    return user
    


# def get_current_active_user(request: Request, db: Session = Depends(get_db)):
#     token = request.cookies.get("access_token")
#     if not token:
#         print("Token not found in cookies")
#         raise credentials_exception
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             print("Username not found in token payload")
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         print("JWT Error: Invalid token")
#         raise credentials_exception
    # user = db.query(User).filter(User.username == token_data.username).first()
    # password = token_data.password
    # if user is None:
    #     raise credentials_exception
    # if (user.hashed_password != pwd_context.verify(password, user.hashed_password)):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Password do not mach",
    #     )
    # return user

    
    
def get_logged_user(user: UserCreate = Depends(get_current_active_user)):
    
    return user 