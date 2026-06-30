from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.product import Product
from app.models.customer import Customer


def get_total_revenue(db: Session) -> float:
    revenue = db.query(func.sum(Sale.total_amount)).scalar()
    return revenue or 0


def get_dashboard_summary(db: Session) -> dict:
    return {
        "products": db.query(Product).count(),
        "sales": db.query(Sale).count(),
        "revenue": get_total_revenue(db)
    }


def get_top_products(db: Session, limit: int = 5) -> list:
    products = db.query(
        Product.name,
        func.sum(SaleItem.quantity).label("sold")
    ).join(
        SaleItem, Product.id == SaleItem.product_id
    ).group_by(Product.name).order_by(
        desc(func.sum(SaleItem.quantity))
    ).limit(limit).all()

    return [{"product": p.name, "sold": p.sold} for p in products]


def get_monthly_sales(db: Session) -> list:
    results = db.query(
        func.strftime("%Y-%m", Sale.created_at).label("month"),
        func.sum(Sale.total_amount).label("total")
    ).group_by(
        func.strftime("%Y-%m", Sale.created_at)
    ).order_by(
        func.strftime("%Y-%m", Sale.created_at).desc()
    ).all()

    return [{"month": r.month, "total": float(r.total)} for r in results]


def get_category_sales(db: Session) -> list:
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


def get_customer_growth(db: Session) -> list:
    results = db.query(
        func.strftime("%Y-%m", Sale.created_at).label("month"),
        func.count(func.distinct(Sale.customer_id)).label("new_customers")
    ).group_by(
        func.strftime("%Y-%m", Sale.created_at)
    ).order_by(
        func.strftime("%Y-%m", Sale.created_at).desc()
    ).all()

    return [{"month": r.month, "new_customers": r.new_customers} for r in results]


def get_outstanding_credit(db: Session) -> list:
    customers = db.query(Customer).filter(
        Customer.credit_balance > 0
    ).order_by(Customer.credit_balance.desc()).all()

    return [
        {"id": c.id, "name": c.name, "credit_balance": c.credit_balance}
        for c in customers
    ]
