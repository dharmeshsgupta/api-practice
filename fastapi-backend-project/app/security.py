import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from pwdlib import PasswordHasher

load_dotenv()

SECRET_KEY = os.environ["JWT_SECRET_KEY"]
Algorithm = "HS256"
password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=30)
    
    payload = {
        "exp": expires,
        "sub": str(user_id),
    } 
    return jwt.encode(payload, SECRET_KEY, algorithm=Algorithm)