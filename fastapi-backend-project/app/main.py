from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import engine, Base
from app import models
from app.routers import tasks, auth, ai

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    
app = FastAPI(
    title="Task Management API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(ai.router)

@app.get("/")
def home():
    return {"message": "Task Management API is running"}