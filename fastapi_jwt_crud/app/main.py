from fastapi import FastAPI
from app.database import engine, Base
from . import models

from app.auth import router as auth_router
from app.crud import router as items_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI JWT Authrntication and CRUD Application",
)

app.include_router(auth_router)
app.include_router(items_router)

@app.get("/")
def home():
    return {
        "message": "Welcome to the FastAPI JWT Authentication and CRUD Application!"
    }