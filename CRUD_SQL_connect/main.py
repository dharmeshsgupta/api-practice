from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User
from pydantic import BaseModel

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Database dependency
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()
        
# Request Schema
class UserSchema(BaseModel):
    name: str
    email: str
    age: int
        
@app.post("/users/")
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    data = User(**user.model_dump())
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

@app.get("/users")
def read_user(db: Session =  Depends(get_db)):
    return db.query(User).all

@app.get("/users/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(404, "User not found")
    
    return user

@app.put("/users/{id}")
def update_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(404, "User not found")
    
    for key, value in user.model_dump().items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user

# Delete user
@app.delete("/users/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(404, "User not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}