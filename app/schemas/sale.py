from pydantic import BaseModel
from typing import List, Optional


class SaleItemCreate(BaseModel):
    product_id: int
    quantity: int


class SaleCreate(BaseModel):
    customer_id: Optional[int] = None
    items: List[SaleItemCreate]