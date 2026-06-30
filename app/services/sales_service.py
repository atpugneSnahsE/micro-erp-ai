from datetime import datetime
from sqlalchemy.orm import Session

from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.product import Product


def get_all_sales(db: Session):
    return db.query(Sale).all()


def get_sale(db: Session, sale_id: int):
    return db.query(Sale).filter(Sale.id == sale_id).first()


def create_sale(db: Session, customer_id: int | None, items: list[dict]) -> dict:
    total_amount = 0
    new_sale = Sale(customer_id=customer_id, total_amount=0)
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)

    for item in items:
        product = db.query(Product).filter(Product.id == item["product_id"]).first()
        if not product:
            db.rollback()
            raise ValueError(f"Product {item['product_id']} not found")
        if product.quantity < item["quantity"]:
            db.rollback()
            raise ValueError(f"Not enough stock for {product.name}")

        product.quantity -= item["quantity"]
        item_total = product.price * item["quantity"]
        total_amount += item_total

        sale_item = SaleItem(
            sale_id=new_sale.id,
            product_id=product.id,
            quantity=item["quantity"],
            price=product.price
        )
        db.add(sale_item)

    new_sale.total_amount = total_amount
    db.commit()
    db.refresh(new_sale)

    return {
        "sale_id": new_sale.id,
        "total_amount": total_amount
    }


def get_today_sales(db: Session) -> float:
    today = datetime.utcnow().date()
    sales = db.query(Sale).all()
    return round(
        sum(s.total_amount for s in sales if s.created_at.date() == today),
        2
    )
