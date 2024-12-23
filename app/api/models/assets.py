from sqlalchemy import Integer, Column, DateTime, String, ForeignKey, Float
from sqlalchemy.orm import Session, Mapped, mapped_column, relationship

from core.database import Base



# class ServiceType(Base):
#     __tablename__ = 'service_types'
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255))
#     code = Column(String(30), unique=True)

#     service_type = relationship("Service", back_populates='service_type')

#     def __repr__(self):
#         return self.name

# class Service(Base):
#     __tablename__ = "services"
#     id = Column(Integer, primary_key=True, index=True)
#     service_type_idfk = Column(ForeignKey('service_types.id', ondelete="CASCADE"))
#     name = Column(String(255))
#     code = Column(String(100), unique=True)
#     price: Mapped['float'] = mapped_column(Float)
   
#     service_type = relationship("ServiceType", back_populates='service')


#     def __repr__(self):
#         return self.name


# class Product(Base):
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255))

#     material_type = Column(String(255))
#     manufacturer = Column(String(255))
#     sale_margin = Column(Float)

#     inventory = relationship('Inventory', back_populates='product')


#     def __repr__(self):
#         return self.name

# class Inventory(Base):
#     id = Column(Integer, primary_key=True, index=True)
#     product_idfk = Column(ForeignKey('products.id', ondelete='CASCADE'))
#     quantity = Column(Float)
#     buy_unit_price = Column(Float)
#     sale_margin = Column(Float)

#     product = relationship('Product', back_populates='inventory')


#     def __repr__(self):
#         return f"inventory: {self.id} quantity: {self.quantity}"
