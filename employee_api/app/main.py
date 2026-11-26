from fastapi import FastAPI
from app.routers import employees

app = FastAPI(
    title="employee Management API",
    description="Simple FastAPI CRUD API for interview practice",
    version="1.0.0",
)

app.include_router(employees.router)

@app.get("/")
def home():
    return {"message": "Employee Management API is running"}