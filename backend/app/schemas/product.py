from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ProductBase(BaseModel):
    brand: str
    name: str
    type: str
    ingredients: Optional[List[str]] = None
    notes: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    brand: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    ingredients: Optional[List[str]] = None
    notes: Optional[str] = None


class Product(ProductBase):
    id: int
    user_id: Optional[int] = None
    usage_count: int
    success_rate: float
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
