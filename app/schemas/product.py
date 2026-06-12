from pydantic import BaseModel
from typing import Optional


class ProductCreate(BaseModel):
    name: str
    sku: str
    category: str
    quantity: int
    price: float
    reorder_level: int = 5


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    category: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    reorder_level: Optional[int] = None