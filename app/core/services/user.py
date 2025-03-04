from api.models.user import UserModel 
from fastapi.exceptions import HTTPException

from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from core.security import get_password_hash
from api.models import User
from api.schemas import UserCreate


async def create_user_account(data, db):
    user = db.query(UserModel).filter(UserModel.email == data.email).first()

    if user:
        raise HTTPException(
            status_code=422,
            detail="Email is already regisgtered with us.",
        )

    new_user = UserModel(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        password=get_password_hash(data.password),
        role=data.role,
        is_active=False,
        is_verified=False,
        registered_at=datetime.now(),
        updated_at=datetime.now(),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_user_info(db: Session, id:int, data: UserCreate):
    try:
        user = db.query(User).filter_by(id=id).first()
        if user:
            user.username = data.username
            user.email = data.email 
            user.hashed_password = get_password_hash(data.password)
            user.role_id = data.role_id
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        db.commit()
        return None  