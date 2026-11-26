from typing import Dict
from app.schemas import EmployeeCreate, EmployeeUpdate
from fastapi import HTTPException, status

employees: Dict[int, dict] = {}
next_id = 1

def get_all_employees():
    return list(employees.values())

def get_employee(employee_id: int):
    if employee_id not in employees:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found", )
    return employees[employee_id]

def create_employee(employee: EmployeeCreate):
    global next_id
    employee_data = employee.model_dump()
    employee_data["id"] = next_id
    
    employees[next_id] = employee_data
    next_id += 1
    return employee_data

def update_employee(employee_id: int, employee: EmployeeUpdate):
    existing_employee = get_employee(employee_id)
    update_data = employee.model_dump(exclude_unset=True)
    existing_employee.update(update_data)
    return existing_employee

def delete_employee(employee_id: int):
    get_employee(employee_id)
    del employees[employee_id]
    return {"message": "Employee deleted successfully"}