from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserOut
from app.security import (
    hash_password,
    verify_password,
    create_access_token,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: UserOut,
    status_code=status.HTTP_201_CREATED,
):
    existing = db.scalar(
        select(User).where(User.email == data.email)
    )
    
    if existing:
        raise HTTPException(
            status_code=409,
            detail="Email already registered",
        )
    user = User(
        email=str(data.email),
        hashed_password=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

@router.post("/login")
def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(Get_db)],
):
    user = db.scalar(
        select(User).where(User.email == form.username)
    )
    
    if user is None or not verify_password(
        form.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "access_token": create_access_token(user.id),
        "token_type": "bearer",
    }