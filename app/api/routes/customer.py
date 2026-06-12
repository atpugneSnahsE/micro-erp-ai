from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/customers")
def get_customers(
    db: Session = Depends(get_db)
):
    return db.query(Customer).all()


@router.post("/customers")
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):

    new_customer = Customer(
        name=customer.name,
        phone=customer.phone,
        email=customer.email,
        address=customer.address,
        credit_balance=customer.credit_balance
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer