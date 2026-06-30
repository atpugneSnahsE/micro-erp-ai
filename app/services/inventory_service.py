from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.product import Product


def get_all_products(db: Session):
    return db.query(Product).all()


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def get_low_stock_products(db: Session):
    return db.query(Product).filter(
        Product.quantity <= Product.reorder_level
    ).all()


def search_products(db: Session, query: str):
    return db.query(Product).filter(
        or_(
            Product.name.ilike(f"%{query}%"),
            Product.sku.ilike(f"%{query}%"),
            Product.category.ilike(f"%{query}%")
        )
    ).all()


def create_product(db: Session, **kwargs):
    product = Product(**kwargs)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product_id: int, **kwargs):
    product = get_product(db, product_id)
    if not product:
        return None
    for key, value in kwargs.items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    if not product:
        return False
    db.delete(product)
    db.commit()
    return True
