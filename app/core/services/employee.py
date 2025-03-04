from api.models import Employee, Role, User
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session 
from sqlalchemy.exc import SQLAlchemyError
# from core.security import get_password_hash
from datetime import datetime
from core.deps import get_db 
from api.schemas import EmployeeForm



async def create_employee(db:Session, data:EmployeeForm):
    employee = db.query(Employee).filter(Employee.email == data.email).first()

    if employee:
        raise HTTPException(
            status_code=422,
            detail="Employee's email or phone already exists.",
        )

    new_employee = Employee(
        fname=data.first_name,
        mname=data.last_name,
        lname=data.last_name,
        email=data.email,
        dob=data.dob,
        phone=data.phone,
        zipcode=data.zipcode,
        employed_date=data.date_employed,
        profession_name=data.profession_name,
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee



async def update_employee_info(db:Session, data:EmployeeForm):
    try:
        employee:Employee = db.query(Employee).filter_by(email=data.email).first()

        if employee:
            employee.fname=data.first_name,
            employee.mname=data.last_name,
            employee.lname=data.last_name,
            employee.email=data.email,
            employee.dob=data.dob,
            employee.phone=data.phone,
            employee.zipcode=data.zipcode,
            employee.employed_date=data.date_employed,
            employee.profession_name=data.profession_name,
        db.commit()
        print("Update sucessfull")
 
        return employee
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Transaction failed: {e}")
        return None


async def update_user_role(db:Session, role_name:str, user_id: int):
    db_role = db.query(Role).filter(Role.name==role_name).first()
    if db_role:
        try:
            updated_user = db.query(User).filter(User.id==user_id).first()
            if updated_user:
                updated_user.role_id = db_role.id
                db.commit()
                print("User role updated successfully!")
                return updated_user
            
        except Exception as e:
            print("SQLAlchemy Error", e)
            db.rollback()
   
    return {"user": []}
