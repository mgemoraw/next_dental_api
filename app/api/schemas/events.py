from pydantic import BaseModel 
from typing import Optional 
from datetime import datetime
from . import User

class EventBase(BaseModel):
    date: datetime
    name: str 
    description: str

class Event(EventBase):
    created_by: Optional['str']  # creater user first name and last name
    created_at: datetime
    updated_by: Optional['str']  # updater user first name and last name
    updated_at: datetime

    class Config:
        from_attributes=True
    


