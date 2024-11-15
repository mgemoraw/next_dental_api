from pydantic import BaseModel
from typing import Optional


class Address(BaseModel):
    id: int
    city: str
    woreda: str
    zone: str
    state: str
    country: str
    geo: Optional['GeoLocation']
    street: str
    house_number: str
    zipcode: str

class GeoLocation(BaseModel):
    id: int
    lat: str
    lng: str

