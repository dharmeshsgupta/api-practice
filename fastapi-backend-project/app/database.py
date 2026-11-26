import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclartiveBase, sessionmaker

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflash=False,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass

class get_db():
    db = SessionLocal()
    
    try:
        yeild.db
    finally:
        db.close()
        