from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime

from app.database import SessionLocal
from app.models.sale import Sale
from app.models.product import Product
from app.models.sale_item import SaleItem
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


@router.get("/reports/dashboard-summary")
def dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    total_products = db.query(
        Product
    ).count()

    total_sales = db.query(
        Sale
    ).count()

    revenue = db.query(
        func.sum(Sale.total_amount)
    ).scalar()

    return {
        "products": total_products,
        "sales": total_sales,
        "revenue": revenue or 0
    }


@router.get("/reports/today-sales")
def today_sales(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    today = datetime.utcnow().date()

    sales = db.query(Sale).all()

    today_total = 0

    for sale in sales:

        if sale.created_at.date() == today:
            today_total += sale.total_amount

    return {
        "today_sales": round(
            today_total,
            2
        )
    }


@router.get("/reports/top-products")
def top_products(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    products = db.query(
        Product.name,
        func.sum(SaleItem.quantity)
    ).join(
        SaleItem,
        Product.id == SaleItem.product_id
    ).group_by(
        Product.name
    ).order_by(
        desc(func.sum(SaleItem.quantity))
    ).limit(5).all()

    return [
        {
            "product": p[0],
            "sold": p[1]
        }
        for p in products
    ]