
from datetime import datetime, date, timedelta, timezone
from jose import jwt, JWTError
from api.schemas.dental_schemas import UserCreate as User
from core.deps import bcrypt_context, user_dependency, db_dependency
from core.config import get_settings


# get environment variable settings
settings = get_settings()

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
