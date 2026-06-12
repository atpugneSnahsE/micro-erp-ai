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
from app.schemas.sale import SaleCreate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/sales")
def create_sale(
    sale: SaleCreate,
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

    return {
        "sale_id": new_sale.id,
        "total_amount": total_amount,
        "message": "Sale completed"
    }