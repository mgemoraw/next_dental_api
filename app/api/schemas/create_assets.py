from pydantic import BaseModel 
from typing import Optional



class ServiceTypeCreate(BaseModel):
    name: str
    code: str

    class Config:
        orm_mode = True


class ServiceCreate(BaseModel):
    service_type_idfk: int
    name: str
    code: str
    price: float


    class Config:
        orm_mode = True


class ProductCreate(BaseModel):
    name: str
    material_type: str
    manufacturer: str
    sale_margin: float

    class Config:
        orm_mode = True


class InventoryCreate(BaseModel):
    product: Optional[ProductCreate]
    quantity: float
    buy_unit_price: float
    sale_margin: float

    class Config:
        orm_mode = True
