from datetime import timedelta
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jwt.exceptions import InvalidTokenError
from typing import Annotated
from sqlalchemy.orm import Session


from api.schemas import ProductCreate, ServiceCreate, ServiceTypeCreate, InventoryCreate, UserLogin
from api.auth import user_dependency
from api.auth.authentication import get_current_active_user
from core import get_db
from api.models import Product, Service, ServiceType, Inventory, User

from fastapi.responses import JSONResponse


router = APIRouter(
    prefix="/dental/api/v1",
    tags=["assets"],
    responses={404: {"description": "Not Found"}},
)

@router.get("/")
async def greetings():
    return {"data": "Greeting Assets"}


@router.post("/products/create", response_model = None)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(
        name=product.name,
        material_type=product.material_type,
        manufacturer=product.manufacturer,
        sale_margin=product.sale_margin,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.get("/products/index", response_model = None)
async def get_products(limit: int = 10, db: Session = Depends(get_db)):
    products = db.query(Product).limit(limit).all()
    if products:
        return products
    return {"products": []}


@router.delete("/products/delete/{id}", response_model = None)
async def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if product is not None:
        db.delete(product)
        db.commit()
        db.refresh(product)
        return product
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    
@router.post("/services/create", response_model=None)
async def create_service(service: ServiceCreate, user: user_dependency, db: Session = Depends(get_db)):
    new_service = Service(
        service_type_idfk=service.service_type_idfk,
        name=service.name,
        code=service.code,
        price=service.price,
    )
    if service:
        db.add(new_service)
        db.commit()
        db.refresh(new_service)
    return new_service

@router.get("/services/index", response_model = None)
async def get_services(user:User = Depends(get_current_active_user), limit: int = 10, db: Session = Depends(get_db) ):
    services = db.query(Service).limit(limit).all()
    if services:
        return services
    return {"services": []}


@router.delete("/services/delete/{id}", response_model=None)
async def delete_service(user: user_dependency, id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == id).first()
    if service is not None:
        db.delete(service)
        db.commit()
        db.refresh(service)
        return service
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found",
        )


@router.post("/service_types/create", response_model = None)
async def create_service_type(service_type: ServiceTypeCreate, user: user_dependency, db: Session = Depends(get_db)):
    new_service_type = ServiceType(
        name=service_type.name,
        code=service_type.code,
    )

    db.add(new_service_type)
    db.commit()
    db.refresh(new_service_type)
    return new_service_type

@router.get("/service_types/index", response_model = None)
async def get_service_types(user: user_dependency, limit: int = 10, db: Session = Depends(get_db)):
    service_types = db.query(ServiceType).limit(limit).all()
    if service_types:
        return service_types
    return {"service_types": []}

@router.delete("/service_types/delete/{id}", response_model = None)
async def delete_service_type(user: user_dependency, id: int, db: Session = Depends(get_db)):
    service_type = db.query(ServiceType).filter(ServiceType.id == id).first()
    if service_type is not None:
        db.delete(service_type)
        db.commit()
        db.refresh(service_type)
        return service_type
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service Type not found",
        )
    

@router.post("/inventories/create", response_model = None)
async def create_inventory(inventory: InventoryCreate, user: user_dependency, db: Session = Depends(get_db)):
    new_inventory = Inventory(
        product = inventory.product,
        quantity=inventory.quantity,
        buty_unit_price=inventory.buy_unit_price,
        sale_margin=inventory.sale_margin,
    )

    db.add(new_inventory)
    db.commit()
    db.refresh(new_inventory)
    return new_inventory


@router.get("/inventories/index", response_model = None)
async def get_inventories(user: user_dependency, limit: int = 10, db: Session = Depends(get_db)):
    inventories = db.query(Inventory).limit(limit).all()
    if inventories:
        return inventories
    return {"inventories": []}


@router.delete("/inventries/delete/{id}", response_model = None)
async def delete_inventory(user: user_dependency, id: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.id == id).first()
    if inventory is not None:
        db.delete(inventory)
        db.commit()
        db.refresh(inventory)
        return inventory
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory not found",
        )
