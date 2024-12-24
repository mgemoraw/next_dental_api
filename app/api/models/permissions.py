from sqlalchemy import Column, Integer, String, ForeignKey, Table

from sqlalchemy.orm import relationship, sessionmaker
from fastapi import FastAPI

from core import Base


role_permissions = Table(
    'role_permissions', 
    Base.metadata,    
    Column('role_id', Integer, ForeignKey('roles.id')),    
    Column('permission_id', Integer, ForeignKey('permissions.id'))
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)    
    password = Column(String)   
    role_id = Column(Integer, ForeignKey('roles.id'))    
    role = relationship("Role", back_populates="users")

