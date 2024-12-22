""" dental system data models """
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ServiceType(BaseModel):
    name: str
    code: str

    class Config:
        orm_mode = True


class Service(BaseModel):
    service: Optional[ServiceType]
    name: str
    code: str
    price: float


    class Config:
        orm_mode = True


class Product(BaseModel):
    name: str
    material_type: str
    manufacturer: str
    sale_margin: float

    class Config:
        orm_mode = True


class Inventory(BaseModel):
    product: Product
    quantity: float
    buy_unit_price: float
    sale_margin: float

    class Config:
        orm_mode = True


class Patient(BaseModel):
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
    patient: Patient
    appointment_date: datetime
    discharged_date: datetime
    description: str
    appointment_type: str # checkup follow-up treatment other
    patient_notified: bool # true/false, default false,
    doctor: Optional['Doctor']
    status: str # admited, compmleted, appointed, cancelled

    class Config:
        orm_mode = True


class AppointmentService(BaseModel):
    # treatment
    appointment: Optional['Appointment']
    service: Optional['Service']
    treatment: Optional[str]
    status: str # pending, completed, cancelled
    description: str

    class Config:
        orm_mode = True


class TreatmentProduct(BaseModel):
    appointment_service: Optional['AppointmentService']
    product: Optional['Product']
    product_quantity: float
    class Config:
        orm_mode = True


class Billing(BaseModel):
    appointment: Optional['Appointment']
    billing_date: datetime
    payment_plan: str


    class Config:
        orm_mode = True


class BillingAppointmentService(BaseModel):
    billing: Optional['Billing']
    billing_appointment_service_id: str
    service_or_product_id: str

    unit_price: float
    quantity: int
    payment_plan: str

    class Config:
        orm_mode = True


class Payment(BaseModel):
    billing: Optional['Billing']
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
    user: Optional['User']
    contact: Optional['Contact']
    employed_date: datetime
    department: str # department name given in the clinic

    class Config:
        orm_mode = True


class Doctor(Employee):
    did: str
    speciality: str

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


class User(BaseModel):
    username: str
    email: str
    hashed_password: str
    role: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str

    class Config:
        orm_mode = True

