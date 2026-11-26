from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, security, schemas
from app.database import get_db
from app.security import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=schemas.UserOut, status_code=201)
def register(user:schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(
        (models.User.username == user.username) | 
        (models.User.email == user.email)
    ).first()

    if existing_user:
        raise HTTPExeption(
            detail="Username or email already exists",
            status_code=status.HTTP_400_BAD_REQUEST
        )
        
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=security.hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(
        models.User.username == form.username
    ).first()
    if not user:
        raise HTTPException(
            ststus_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    if not security.verify_password(form.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    access_token = security.create_access_token(
        data={"sub": user.username}

    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    