from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    sku = Column(String, unique=True, nullable=False)

    category = Column(String)
    quantity = Column(Integer, default=0)

    price = Column(Float, nullable=False)

    reorder_level = Column(Integer, default=5)