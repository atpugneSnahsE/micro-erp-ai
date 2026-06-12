from sqlalchemy import Column, Integer, String
from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    phone = Column(String)
    email = Column(String)

    address = Column(String)

    credit_balance = Column(Integer, default=0)