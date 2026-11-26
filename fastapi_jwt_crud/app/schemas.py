from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr 
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel): 
    access_token: str
    token_type: str = "bearer"

class ItemCreate(BaseModel):
    title: str
    description: str | None = None



# 1. Define the base class first!
class ItemBase(BaseModel):
    title: str
    description: str | None = None


# This is the serialization schema used for outgoing API responses
class ItemResponse(ItemBase):
    id: int
    owner_id: int

    class Config:
        # Allows Pydantic to read SQLAlchemy lazy-loaded attributes automatically
        from_attributes = True 

class ItemOut(BaseModel):
    id: int
    title: str
    description: str | None = None
    owner_id: int

    class Config:
        from_attributes = True

# Add this inside app/schemas.py
class ItemUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
