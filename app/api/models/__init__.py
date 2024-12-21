from .employee import Employee, Doctor
from .patient import Patient
from .user import UserModel, User
from .posts import Post

from core.database import Base, engine

__all__ = [
    Employee,
    Patient,
    User,
    UserModel,
    Doctor,
]

Base.metadata.create_all(engine)
