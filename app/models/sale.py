from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=True
    )

    total_amount = Column(Float, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    customer = relationship("Customer")