from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, security
from app.database import get_db
from app.security import get_current_user
# Add this import at the top of app/crud.py
from app import schemas


router = APIRouter(
    prefix="/items",
    tags=["Items"]
)

@router.post("/", response_model=schemas.ItemResponse, status_code=201)
def create_item(
    item: schemas.ItemCreate,
    db:Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_item = models.Item(
        title=item.title,
        description=item.description,
        owner_id=current_user.id
    )
    db.add(new_item)
    db.commit()
    db.refrsh(new_item)
    return new_item

@router.get("/", response_model=list[schemas.ItemOut])
def get_all_items(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Items).filter(models.Item.owner_id == current_user.id).all()

@router.get("/{item_id}", response_model=schemas.ItemOut)
def get_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    item = db.query(models.Items).filter(
        models.Item.id == item_id,
        models.Item.owner_id == current_user.id
    ).first()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return item

@router.put("/{item_id}", response_model=schemas.ItemOut)
def update_item(
    item_id: int, 
    update_data: schemas.ItemUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    items = db.query(models.Item).filter(
        models.Item.id == item_id,
        models.Item.order_id == current_user.id
    ).first()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)

    return item

@router.delete("/{item_id}", status_code=204)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    item = db.query(models.Item).filter(
        models.Item.id == item_id,
        models.Item.owner_id == current_user.id
    ).first()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    db.delete(item)
    db.commit()
    