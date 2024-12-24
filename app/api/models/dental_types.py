from sqlalchemy import ForeignKey, String, Integer, Float
from core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List


class ServiceType(Base):
    __tablename__ = "service_types"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    code: Mapped[str]  = mapped_column(String(100))

    # relationship
    services: Mapped[List['Service']] = relationship('Service', back_populates='service_type')


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    service_type_idfk: Mapped[int] = mapped_column(ForeignKey('service_types.id', ondelete='CASCADE'))
    name: Mapped[str] = mapped_column(String(100))
    code: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)
    # relationship
    service_type: Mapped['ServiceType'] = relationship('ServiceType', back_populates='services')

    def __repr__(self):
        return self.name


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    material_type: Mapped[str] = mapped_column(String(100))
    manufacturer: Mapped[str] = mapped_column(String(100))
    sale_margin: Mapped[float] = mapped_column()

    # relationship
    inventory: Mapped['Inventory'] = relationship('Inventory', back_populates='products')


class Inventory(Base):
    __tablename__ = "inventories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_idfk: Mapped[Optional[int]] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'))
    quantity: Mapped[float] = mapped_column(default=0.0)
    buy_unit_price: Mapped[float] = mapped_column(default=0.0)
    sale_margin: Mapped[float] = mapped_column(default=0.0)

    # relationship
    products: Mapped[List[Product]] = relationship('Product', back_populates='inventory')



