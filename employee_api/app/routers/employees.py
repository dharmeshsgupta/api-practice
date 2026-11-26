from typing import List
from fastapi import APIRouter, status

from app import storage
from app.schemas import EmployeeCreate, EmployeeUpdate, EmployeeResponse

router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)

@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeCreate):
    return storage.create_employee(employee)

@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int):
    return storage.get_employee(employee_id)


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int, employee: EmployeeUpdate):
    return storage.update_employee(employee_id, employee)

@router.delete("/{employee_id}")
def delete_employee(employee_id: int):
    return storage.delete_employee(employee_id)