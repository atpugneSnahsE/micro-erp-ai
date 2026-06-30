from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.database import SessionLocal
from app.models.user import User
from app.models.customer import Customer
from app.models.customer_note import CustomerNote
from app.models.sale import Sale
from app.services.dependencies import get_current_user
from app.services.audit import log_action

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class NoteCreate(BaseModel):
    note: str


@router.get("/crm/customers/{customer_id}/notes")
def get_customer_notes(
    customer_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db.query(CustomerNote).filter(
        CustomerNote.customer_id == customer_id
    ).all()


@router.post("/crm/customers/{customer_id}/notes")
def create_customer_note(
    customer_id: int,
    note_data: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    note = CustomerNote(
        customer_id=customer_id,
        note=note_data.note,
        created_by=current_user.id
    )
    db.add(note)
    db.commit()
    db.refresh(note)

    log_action(db, current_user.id, "Created note", "customer_notes", note.id)

    return note


@router.get("/crm/customers/{customer_id}/history")
def get_customer_history(
    customer_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return db.query(Sale).filter(
        Sale.customer_id == customer_id
    ).order_by(Sale.created_at.desc()).all()


@router.get("/crm/top-customers")
def get_top_customers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
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
    ).limit(10).all()

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
