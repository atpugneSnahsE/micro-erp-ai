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
from app.models.customer import Customer
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


@router.get("/reports/monthly-sales")
def monthly_sales(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    results = db.query(
        func.strftime("%Y-%m", Sale.created_at).label("month"),
        func.sum(Sale.total_amount).label("total")
    ).group_by(
        func.strftime("%Y-%m", Sale.created_at)
    ).order_by(
        func.strftime("%Y-%m", Sale.created_at).desc()
    ).all()

    return [{"month": r.month, "total": float(r.total)} for r in results]


@router.get("/reports/category-sales")
def category_sales(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    results = db.query(
        Product.category,
        func.sum(SaleItem.quantity).label("quantity_sold"),
        func.sum(SaleItem.quantity * SaleItem.price).label("revenue")
    ).join(
        SaleItem, Product.id == SaleItem.product_id
    ).group_by(Product.category).order_by(
        desc(func.sum(SaleItem.quantity * SaleItem.price))
    ).all()

    return [
        {
            "category": r.category,
            "quantity_sold": r.quantity_sold,
            "revenue": float(r.revenue) if r.revenue else 0
        }
        for r in results
    ]


@router.get("/reports/customer-growth")
def customer_growth(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    results = db.query(
        func.strftime("%Y-%m", Sale.created_at).label("month"),
        func.count(func.distinct(Sale.customer_id)).label("new_customers")
    ).group_by(
        func.strftime("%Y-%m", Sale.created_at)
    ).order_by(
        func.strftime("%Y-%m", Sale.created_at).desc()
    ).all()

    return [{"month": r.month, "new_customers": r.new_customers} for r in results]


@router.get("/reports/outstanding-credit")
def outstanding_credit(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    customers = db.query(Customer).filter(
        Customer.credit_balance > 0
    ).order_by(Customer.credit_balance.desc()).all()

    return [
        {"id": c.id, "name": c.name, "credit_balance": c.credit_balance}
        for c in customers
    ]
