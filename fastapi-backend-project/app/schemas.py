from pydantic import BaseModel, ConfigDict,  Field, EmailStr

class UserCreate(BaseModel):
    email: EmailStr 
    password: str = Field(min_length=8, max_length=128)
    
class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    
class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    completed: bool | None = None
    
class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str | None
    completed: bool
    owner_id: int
    created_at: str