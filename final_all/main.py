from fastapi import FastAPI, HTTPException, Depends, HTTPException
from fastapi.security import  OAuth2PasswordBearer
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
# from database import SessionLocal, engine, Base
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


app = FastAPI()

#DAtabase
DATABASE_URL = "postgresql://postgres:Dharmesh123@localhost:5432/testdb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    bind = engine,
    autocommit = False,
    autoflush = False,
)
Base = declarative_base()

# JWT Configuration
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# DATABASE MODELS
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

Base.metadata.create_all(bind=engine)

# Request schemas
class UserSchema(BaseModel):
    username: str
    password: str
    
class ItemSchema(BaseModel):
    name: str
    
# Database Dependency
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
        
# Register
@app.post("/register")
def register(data: UserSchema, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(
        username=data.username,
        password=pwd_context.hash(data.password)
    )
    db.add(user)
    db.commit()
    return {"message": "Registered"}

@app.post("/login")
def login(data: UserSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=data.username).first()
    
    if not user or not pwd_context.verify(data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = jwt.encode(
        {"sub": str(user.id)}, SECRET_KEY, algorithm=ALGORITHM
    )
    return {"access_token": token, "token_type": "bearer"}

# Verify JWT
from fastapi.security import OAuth2PasswordBearer

oauth = OAuth2PasswordBearer(tokenUrl="/login")
def get_current_user(token: str = Depends(oauth), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = db.query(User).filter_by(id=int(payload["sub"])).first()
        if not user: 
            raise HTTPException(status_code=401, detail="Invalid token")
        return user
    except(JWTError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")
    
#Crud
#Create Item
@app.post("/items")
async def create_item(
    data: ItemSchema,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = Item(
        name=data.name,
        user_id=user.id
    )
    db.add(item)
    db.commit()
    return {"message": "Item created"}

@app.get("/items")
async def get_items(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Item).filter_by(user_id= user.id).all()

@app.put("/items/{id}")
async def update_item(
    id: int, 
    data: ItemSchema,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Item).filter_by(id=id, user_id=user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.name = data.name
    db.commit()
    db.refresh(item)
    return item

@app.delete("/items/{id}")
async def delete_item(
    id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Item).filter_by(id=id, user_id=user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Deleted"}