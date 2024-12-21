from pydantic import BaseModel
from typing import Optional
from .address import Address
from datetime import datetime


class Employee(BaseModel):
    id: int
    employee_id: str
    first_name: str
    middle_name: str
    last_name: str
    email: str
    phone: str
    field_of_study: str
    employed_date: datetime 
    salary: float
    address: Optional['Address']
    zipcode: str

class EmployeeForm(BaseModel):
    id: int
    employee_id: str
    first_name: str
    middle_name: str
    last_name: str
    email: str
    phone: str
    address: Optional['Address']
    zipcode: str

