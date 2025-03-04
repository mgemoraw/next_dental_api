from datetime import timedelta
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status, Response, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

# from jwt.exceptions import InvalidTokenError
from typing import Annotated
from sqlalchemy.orm import Session
from api.schemas import UserLogin, Token, EmployeeForm
from api.auth.authentication import (
    authenticate_user, 
    create_access_token, 
    get_current_active_user, 
    get_current_user,
    role_required,
)

from api.models import User, Role
from api.auth.utils import create_user, get_user_by_username
from api.schemas.dental_schemas import UserCreate
from api.models.employee import Employee
from core.services.user import update_user_info
from core import get_db
from core.services.employee import (
    create_employee, 
    update_employee_info,
)

ACCESS_TOKEN_EXPIRE_MINUTES = 300

router = APIRouter(
    prefix="/dental/api/v1",
    tags=["employees", "users"],
    responses={404: {"description": "Not Found"}},
)


@router.get("/employees")
def greet():
    greeting = {"hello": "Greetings!"}
    return JSONResponse(content=greeting)

@router.post("/employees/login", response_model=Token)
async def user_login(form_data: OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
    # db_user = authenticate_user(user.username, user.password, db)
    db_user = authenticate_user(form_data.username, form_data.password, db)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or passsword",
            headers={"WW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) 
    access_token = create_access_token(
        data = {"sub": db_user.username}, expires_delta=access_token_expires,
    )

    # grab role
    role = db.query(Role).filter(Role.id==db_user.role_id).first()
    # Response content
    content = {
        "access_token": access_token, 
        "token_type": "bearer", 
        "username": db_user.username, 
        "role": role.name,
        }
    
    response = JSONResponse(content=content)
    response.set_cookie(
        key="access_token", 
        value=access_token, 
        httponly=True,
        secure=False,
        samesite='Lax',
        ) 

    # return content
    return response

@router.post("/employees/logout")
async def logout(user: User=Depends(get_current_active_user)):
    response = JSONResponse(content={"message": "Successfully logged out"})
    # Set the cookie with an expired date
    response.delete_cookie(key="access_token")
    
    return response


@router.post("/users/create")
async def register_user(new_user: UserCreate, user:User=Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_role = db.query(Role).filter(User.role_id==user.role_id).first()

    if user_role.name.lower()=="admin":
        db_user = get_user_by_username(db, username=user.username)
        if db_user:
            raise HTTPException(status_code=400, detail="Username exists")
        return await create_user(db=db, user=new_user)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="YOu are not authorized or token expired!",
    )

@router.put("/users/update/{id}")
async def update_user_by_id(user_id: int, data:UserCreate, user:User=Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_role = db.query(Role).filter(User.role_id==user.role_id).first()

    if user_role.name.lower()=="admin":
        db_user = await update_user_info(db=db, user_id=user_id, data=data)
        if not db_user:
            raise HTTPException(status_code=400, detail="Update failed")
        return db_user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="YOu are not authorized or token expired!",
    )


@router.get("/users/index")
async def get_users(user:User = Depends(get_current_active_user), db: Session=Depends(get_db)):

    user_role = db.query(Role).filter(User.role_id==user.role_id).first()

    if user_role.name.lower()=="admin":
        users = db.query(User).all()
        return users
    return {"users": []}

@router.get("/users/me")
async def get_my_info(user:User = Depends(get_current_active_user), db: Session=Depends(get_db)):

    if user:
        db_user = db.query(User).filter(User.id==user.id).first()
        return db_user
    return {"user": []}

@router.delete("users/delete/{id}")
async def delete_user(id:int, user:User = Depends(get_current_active_user), db:Session=Depends(get_db)):
    db_user = db.query(User).filter(User.id==id).first()
    if db_user:
        db.delete()
        db.commit()
        return db_user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found in the database",
    )


@router.get("/users/{id}")
async def get_user_by_id(id:int, user:User = Depends(get_current_active_user), db: Session=Depends(get_db)):
    user_role = db.query(Role).filter(User.role_id==user.role_id).first()

    if user_role.name.lower()=="admin":
        db_user = db.query(User).filter(User.id==id).first()
        return db_user
    return {"user": []}

@router.post("/users/role/update")
async def update_user_role(role: str, user_id: int, user:User = Depends(get_current_active_user), db: Session=Depends(get_db)):
    user_role = db.query(Role).filter(User.role_id==user.role_id).first()
    if user_role.name.lower()=="admin":
        db_role = db.query(Role).filter(Role.name==role).first()
        if db_role:
            try:
                updated_user = db.query(User).filter(User.id==user_id).first()
                if updated_user:
                    updated_user.role_id = db_role.id
                db.commit()
                print("User role updated successfully!")
                return db_role
            except Exception as e:
                print("SQLAlchemy Error", e)
                db.rollback()
   
    return {"role": []}


@router.post("/employees/create")
async def register_employee(employee: EmployeeForm, user:User=Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_role = db.query(Role).filter(User.role_id==user.role_id).first()

    if user_role.name.lower()=="admin":
        db_user = get_user_by_username(db, username=user.username)
        if db_user:
            raise HTTPException(status_code=400, detail="Username exists")
        return await create_employee(db=db, user=employee)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="YOu are not authorized or token expired!",
    )


@router.get("/employees/{id}")
async def get_employee_by_id(id:int, user:User = Depends(get_current_active_user), db: Session=Depends(get_db)):
    user_role = db.query(Role).filter(User.role_id==user.role_id).first()

    if user_role.name.lower()=="admin":
        employee = db.query(Employee).filter(Employee.id==id).first()
        return employee
    return {"employee": []}

@router.get("/employees/me")
async def get_employee_info(user:User = Depends(get_current_active_user), db: Session=Depends(get_db)):

    if user:
        employee = db.query(Employee).filter(Employee.id==user.id).first()
        return employee
    return {"employee": []}

@router.get("/employees/index")
async def get_employees(user:User = Depends(get_current_active_user), db: Session=Depends(get_db)):

    if user:
        employee = db.query(Employee).filter(Employee.id==user.id).first()
        return employee
    return {"employee": []}


@router.delete("employees/delete/{id}")
async def delete_employee(id:int, user:User = Depends(get_current_active_user), db:Session=Depends(get_db)):
    db_user = db.query(Employee).filter(Employee.id==id).first()
    if db_user:
        db.delete()
        db.commit()
        return db_user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Employee not found in the database",
    )


@router.put("employees/update/{id}")
async def update_employee_info(employee:EmployeeForm, user:User = Depends(get_current_active_user), db:Session=Depends(get_db)):
    
    employee = await update_employee_info(db, employee)
    if employee:
        return employee 
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Employee not found in the database",
    )




# # @router.get("/admin/dashboard")
# @router.get("/admin")
# async def admin_dashboard(user:User = Depends(get_current_active_user)):    
#     # role: str = Depends(role_required("Admin"))
#    return {"message": "Welcome to the Admin Dashboard"}

# # @router.get("/dentist/patients")
# @router.get("/dentist")
# async def dentist_patients(user:User = Depends(get_current_active_user)):  
#     # role: str = Depends(role_required("Dentist"))  
#    return {"message": "Access to patient records"}


