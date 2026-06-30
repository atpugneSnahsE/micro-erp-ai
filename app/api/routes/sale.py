from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.product import Product
from app.models.user import User

from app.schemas.sale import SaleCreate

from app.services.audit import log_action
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


@router.get("/sales")
def get_sales(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Sale).all()


@router.post("/sales")
def create_sale(
    sale: SaleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    total_amount = 0

    new_sale = Sale(
        customer_id=sale.customer_id,
        total_amount=0
    )

    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)

    for item in sale.items:

        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product {item.product_id} not found"
            )

        if product.quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for {product.name}"
            )

        product.quantity -= item.quantity

        item_total = (
            product.price * item.quantity
        )

        total_amount += item_total

        sale_item = SaleItem(
            sale_id=new_sale.id,
            product_id=product.id,
            quantity=item.quantity,
            price=product.price
        )

        db.add(sale_item)

    new_sale.total_amount = total_amount

    db.commit()
    db.refresh(new_sale)

    log_action(db, current_user.id, "completed", "sales", new_sale.id)

    return {
        "sale_id": new_sale.id,
        "total_amount": total_amount,
        "message": "Sale completed"
    }


@router.get("/sales/{sale_id}")
def get_sale(
    sale_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    sale = db.query(Sale).filter(
        Sale.id == sale_id
    ).first()

    if not sale:
        raise HTTPException(
            status_code=404,
            detail="Sale not found"
        )

    return sale