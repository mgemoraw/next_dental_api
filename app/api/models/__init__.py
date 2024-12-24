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

from .patient import (
    Role,
    Visit,
    Doctor,
    Permission,
    Payment,
    )

from .events import Event

from core.database import Base, engine


Base.metadata.create_all(bind=engine)
