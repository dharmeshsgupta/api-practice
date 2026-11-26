from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.contact import router as contact_router

app = FastAPI(title="React + FastAPI Form API")

allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(contact_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}