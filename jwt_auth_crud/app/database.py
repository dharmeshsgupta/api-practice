from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

URL = "postgresql+psycopg://postgres:Dharmesh123@localhost:5432/dataint"

engine = create_engine(URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()