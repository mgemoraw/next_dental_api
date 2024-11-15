from pydantic import BaseModel
from typing import Optional
from .address import Address

class Employee(BaseModel):
    id: int
    employee_id: str
    first_name: str
    middle_name: str
    last_name: str
    email: str
    phone: str
    address: Optional['Address']
    zipcode: str

