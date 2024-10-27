from sqlalchemy.orm import Session
from models.item import Item
from pydantic import BaseModel
from typing import List, Optional


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: int

class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: int

    class Config:
        orm_mode = True


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    

def get_health():
    return {
        'detail': 'Hello from your FastAPI app'
    }

def create_item(db: Session, item: ItemCreate):
    db_item = Item(name=item.name, description=item.description, price=item.price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Item).offset(skip).limit(limit).all()

def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def update_item(db: Session, item_id: int, item: ItemUpdate):
    db_item = get_item(db, item_id)
    if not db_item:
        return None
    update_data = item.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = get_item(db, item_id)
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item