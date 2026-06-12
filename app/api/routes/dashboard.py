from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import SessionLocal
from app.models.product import Product
from app.models.customer import Customer
from app.models.sale import Sale

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db)
):

    total_products = db.query(Product).count()

    total_customers = db.query(Customer).count()

    total_sales = db.query(Sale).count()

    revenue = db.query(
        func.sum(Sale.total_amount)
    ).scalar()

    return {
        "products": total_products,
        "customers": total_customers,
        "sales": total_sales,
        "revenue": revenue or 0
    }