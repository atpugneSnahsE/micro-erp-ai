from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from app.database import SessionLocal
from app.models.sale import Sale
from app.models.product import Product
from app.models.user import User

from app.services.dependencies import (
    get_current_user
)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/reports/revenue")
def revenue_report(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    revenue = db.query(
        func.sum(Sale.total_amount)
    ).scalar()

    return {
        "total_revenue": revenue or 0
    }


@router.get("/reports/low-stock")
def low_stock(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    products = db.query(Product).filter(
        Product.quantity <= Product.reorder_level
    ).all()

    return products