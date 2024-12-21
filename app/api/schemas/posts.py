from pydantic import BaseModel
from typing import Optional


class PostCreate(BaseModel):
    user_id: int
    content: str
    class Config:
        orm_mode = True

class PostResponse(BaseModel):
    id: int 
    user_id: int
    content: str 
    
    class Config:
        orm_mode = True 

