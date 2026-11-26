from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class EmployeeCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: str
    department: str
    salary: float = Field(gt=0)
    
class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    salary: Optional[float] = Field(default=None, gt=0)
    
class EmployeeResponse(EmployeeCreate):
    id: int
    
