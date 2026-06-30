from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.customer import Customer
from app.models.user import User

from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate
)

from app.services.dependencies import (
    get_current_user
)

from app.services.permissions import (
    require_admin
)
from app.services.audit import log_action

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/customers")
def get_customers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Customer).all()


@router.post("/customers")
def create_customer(
    customer: CustomerCreate,
    current_user: User = Depends(get_current_user),
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

    log_action(db, current_user.id, "created", "customers", new_customer.id)

    return new_customer


@router.get("/customers/{customer_id}")
def get_customer(
    customer_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


@router.put("/customers/{customer_id}")
def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    update_data = customer_data.dict(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(customer, key, value)

    db.commit()
    db.refresh(customer)

    log_action(db, admin.id, "updated", "customers", customer_id)

    return customer


@router.delete("/customers/{customer_id}")
def delete_customer(
    customer_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    db.delete(customer)
    db.commit()

    log_action(db, admin.id, "deleted", "customers", customer_id)

    return {
        "message": "Customer deleted"
    }