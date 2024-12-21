""" dental system data models """
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ServiceType(BaseModel):
    id: int
    name: str
    code: str

    class Config:
        orm_mode = True

class Service(BaseModel):
    id: int
    service_type_idfk: ServiceType
    name: str
    code: str
    class Config:
        orm_mode = True

class Product(BaseModel):
    id: int
    name: str
    material_type: str
    manufacturer: str
    sale_margin: float

    class Config:
        orm_mode = True


class Inventory(BaseModel):
    id: int
    product_idfk: Product
    quantity: float
    buy_unit_price: float
    sale_margin: float

    class Config:
        orm_mode = True

class Patient(BaseModel):
    id: int
    fname: str
    mname: str
    lname: str
    dob: datetime
    sex: int
    sex_code: int
    sex_text: str
    preferred_language: int
    occupation: str
    address: str
    phone_number: str
    email: str
    previous_medical_condition: str
    emergency_contact: str
    sergical_history: str

    class Config:
        orm_mode = True

class Appointment(BaseModel):
    id: int
    patient_idfk: Patient
    app_date: datetime
    discharged_date: datetime
    description: str
    appointment_type: str # checkup follow-up treatment other
    patient_notified: bool # true/false, default false,
    doctor_idfk: str
    status: str # admited, compmleted, appointed, cancelled

    class Config:
        orm_mode = True

class AppointmentService(BaseModel):
    # treatment
    id: int
    appointment_idfk: Appointment
    service_idfk: str

    status: str # pending, completed, cancelled
    description: str

    class Config:
        orm_mode = True

class TreatmentProduct(BaseModel):
    id: int
    appointment_service_idfk: AppointmentService
    product_idfk: str
    product_quantity: float
    class Config:
        orm_mode = True

class Billing(BaseModel):
    id: int
    appointment_idfk: Appointment
    billing_date: datetime
    payment_plan: str
    class Config:
        orm_mode = True

class BillingAppointmentService(BaseModel):
    id: int
    billing_idfk: Billing
    billing_appointment_service_id: str
    service_or_product_id: str

    unit_price: float
    quantity: int
    payment_plan: str

    class Config:
        orm_mode = True

class Payment(BaseModel):
    id: int
    billing_idfk: str
    payment_date: datetime
    paid_amount: float
    payment_status: str
    class Config:
        orm_mode = True

class Employee(BaseModel):
    fname: str
    mname: str
    lname: str
    sex: str
    address: Optional['Address']
    user: Optional['LoggedUser']
    contact: Optional['Contact']

    class Config:
        orm_mode = True

class Address(BaseModel):
    city: str
    address1: str
    address2: str

    class Config:
        orm_mode = True

class Contact(BaseModel):
    fixed_phone: str
    mobile_phone: str
    email: str

    class Config:
        orm_mode = True

class LoggedUser(BaseModel):
    username: str
    email: str
    hashed_password: str
    role: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    email: str
    password1: str
    password2: str
    role: str

    class Config:
        orm_mode = True

