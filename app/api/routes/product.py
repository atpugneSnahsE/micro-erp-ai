from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_

from app.database import SessionLocal
from app.models.product import Product
from app.models.user import User
from app.schemas.product import ProductCreate

from app.services.dependencies import (
    get_current_user
)

from app.services.permissions import (
    require_admin
)
from app.schemas.product import (
    ProductCreate,
    ProductUpdate
)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/products/low-stock")
def low_stock_products(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Product).filter(
        Product.quantity <= Product.reorder_level
    ).all()

@router.get("/products/search")
def search_products(
    q: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    products = db.query(Product).filter(
        or_(
            Product.name.ilike(f"%{q}%"),
            Product.sku.ilike(f"%{q}%"),
            Product.category.ilike(f"%{q}%")
        )
    ).all()

    return products

@router.get("/products/{product_id}")
def get_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product

@router.get("/products")
def get_products(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Product).all()


@router.post("/products")
def create_product(
    product: ProductCreate,
    admin: User = Depends(require_admin),
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

@router.put("/products/{product_id}")
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    update_data = product_data.dict(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return product

@router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted"
    }
