from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import SessionLocal
from app.models.product import Product
from app.schemas.product import ProductCreate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@router.post("/products")
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):

    new_product = Product(
        name=product.name,
        sku=product.sku,
        category=product.category,
        quantity=product.quantity,
        price=product.price,
        reorder_level=product.reorder_level
    )

    try:
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="SKU already exists"
        )

    return new_product