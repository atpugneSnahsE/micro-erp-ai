import random

from app.database import SessionLocal
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.product import Product


db = SessionLocal()


def create_sale():

    products = db.query(Product).all()

    if not products:
        print("No products found.")
        return

    selected_products = random.sample(
        products,
        random.randint(1, 4)
    )

    total_amount = 0

    new_sale = Sale(
        customer_id=random.randint(1, 4),
        total_amount=0
    )

    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)

    for product in selected_products:

        quantity = random.randint(1, 3)

        if product.quantity < quantity:
            continue

        product.quantity -= quantity

        item_total = (
            product.price * quantity
        )

        total_amount += item_total

        sale_item = SaleItem(
            sale_id=new_sale.id,
            product_id=product.id,
            quantity=quantity,
            price=product.price
        )

        db.add(sale_item)

    new_sale.total_amount = round(
        total_amount,
        2
    )

    db.commit()


for _ in range(25):
    create_sale()

print("Sales seeded successfully!")
