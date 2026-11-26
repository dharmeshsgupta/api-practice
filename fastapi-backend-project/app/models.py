from datetime import datetime

from sqlalchemy import(
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(255), 
        unique=True,
        index=True,
    )
    hashed_password:Mapped[str] = mapped_column(string(255))
    
class Task(Base):
    __tablename__ = "tasks"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"),index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)