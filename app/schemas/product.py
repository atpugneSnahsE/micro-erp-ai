from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    sku: str
    category: str
    quantity: int
    price: float
    reorder_level: int = 5