from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.models.customer import Customer
from app.models.sale import Sale
from app.models.customer_note import CustomerNote


def get_customer_notes(db: Session, customer_id: int):
    return db.query(CustomerNote).filter(
        CustomerNote.customer_id == customer_id
    ).all()


def create_customer_note(db: Session, customer_id: int, note: str, created_by: int):
    note = CustomerNote(
        customer_id=customer_id,
        note=note,
        created_by=created_by
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def get_customer_history(db: Session, customer_id: int):
    return db.query(Sale).filter(
        Sale.customer_id == customer_id
    ).order_by(Sale.created_at.desc()).all()


def get_top_customers(db: Session, limit: int = 10):
    results = db.query(
        Customer.id,
        Customer.name,
        func.count(Sale.id).label("total_purchases"),
        func.sum(Sale.total_amount).label("total_revenue"),
        func.max(Sale.created_at).label("last_purchase")
    ).join(
        Sale, Customer.id == Sale.customer_id
    ).group_by(Customer.id, Customer.name).order_by(
        desc(func.sum(Sale.total_amount))
    ).limit(limit).all()

    return [
        {
            "id": r.id,
            "name": r.name,
            "total_purchases": r.total_purchases,
            "total_revenue": float(r.total_revenue) if r.total_revenue else 0,
            "last_purchase": r.last_purchase.isoformat() if r.last_purchase else None
        }
        for r in results
    ]
