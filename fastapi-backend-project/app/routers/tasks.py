from typing import Annotated

from fastapi import APIRouters, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Task, User
from app.schemas import TaskCreate, TaskUpdate, TaskOut

router = APIRouter(prefix="/tasks", tags=["Tasks"])

DB = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]

@router.post(
    "/",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    data: TaskCreate,
    db: DB,
    user: CurrentUser,
):
    task = Task(
        title=data.title,
        description=data.description,
        owner_id=user.id,
    )
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return task

@router.get("/", response_model=list[TaskOut])
def list_tasks(
    db: DB,
    user: CurrentUser,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge = 1, le=100),
    completed: bool | None = None,
    search: str | None = Query(default=None, max_length=200),
):
    query = select(Task).where(Task.owner_id == user.id)
    
    if completed is not None:
        query = query.where(Task.completed == completed)
        
    if search:
        query = query.where(Task.title.ilike(f"%{search}%"))
        
    query = query.order_by(Task.id).offset(skip).limit(limit)
    return db.scalars(query).all()

@router.get("/{task_id}", response_model=TaskOut)
def get_task(
    task_id: int,
    db: DB,
    user: CurrentUser,
):
    task = db.scalar(
        select(Task).where(
            Task.id == task_id,
            Task.owner == user.id,
        )
    )
    
    if task is None:
        raise HTTPException(status_code=404, detail="Task not Found")
    
    return task

@router.patch("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: DB,
    user: CurrentUser,
):
    task = db.scalar(
        select(Task).where(
            task.id == task_id,
            Task.owner_id == user.id,
        )
    )
    if task is None:
        raise HTTPException(status_code=404, detail="Task not Found")
    
    changes = data.model_dump(exclude_unset=True)
    
    for field, value in changes.items():
        setattr(task, field, value)
        
    db.commit()
    db.refresh(task)
    
    return task

@router.delete("/{task_id}", status_code=status.HTTP_202_NO_CONTENT)
def delete_task(
    task_id: int,
    db: DB,
    user: CurrentUser,
):
    task = db.scalar(
        select(Task).where(
            Task.id == task_id,
            Task.owner_id == user.id,
        )
    )
    
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()