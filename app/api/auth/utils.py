from api.models.user import UserModel
from fastapi.exceptions import HTTPException
from core.security import verify_password


async def get_token(data, db):
    user = db.query(UserModel).filter(UserModel.email==data.email).first() 
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Email not registered",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if verify_password(data.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid login Credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    _verify_usr_access(user=user)

    return '' # Return access token adn refresh token

def _verify_usr_access(user: UserModel):
    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail="Your account is inactive. please contact support",
            headers = {"WWW-Authenticate": "Bearer"}
        )

    if not user.is_verified:
        # user account verification email
        raise HTTPException(
            status_code=400,
            detail="Your account is not verified. We have resent the account verification email",
            headers = {"WWW-Authenticate": "Bearer"},
        )
    

def _get_user_token(user: UserModel, refresh_token=None):
    payload = {'id': user.id}
    