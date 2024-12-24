from .employee import Employee
from .patient import Patient
from .user import UserModel, User
from .posts import Post
from .appointment import Appointment
from .dental_types import (
    Product,
    Service, 
    ServiceType,
    Inventory,
)


from .events import Event

from core.database import Base, engine


__all__ = [
    Employee,
    Patient,
    User,
    UserModel,
]

Base.metadata.create_all(bind=engine)
