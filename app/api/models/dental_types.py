from sqlalchemy import ForeignKey
from core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List


class ServiceType(Base):
    __tablename__ = "service_types"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    code: Mapped[str]  = mapped_column()

    # relationship
    services: Mapped[List['Service']] = relationship(back_populates='service_type')


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    service_type_idfk: Mapped[Optional[int]] = mapped_column(ForeignKey('service_types.id'))
    name: Mapped[str] = mapped_column()
    code: Mapped[str] = mapped_column()

    # relationship
    service_type: Mapped[ServiceType] = relationship(back_populates='service')

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    material_type: Mapped[str]
    manufacturer: Mapped[str]
    sale_margin: Mapped[float]

    # relationship
    inventory: Mapped['Inventory'] = relationship(back_populates='products')


class Inventory(Base):
    __tablename__ = "inventories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_idfk: Mapped[Optional[int]] = mapped_column(ForeignKey('products.id'))
    quantity: Mapped[float] = mapped_column(default=0.0)
    buy_unit_price: Mapped[float] = mapped_column(default=0.0)
    sale_margin: Mapped[float] = mapped_column(default=0.0)

    # relationship
    products: Mapped[List[Product]] = relationship(back_populates='inventory')



