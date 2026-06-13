from app.database import SessionLocal
from app.models.product import Product


db = SessionLocal()


products = [
    {"name": "Rice", "sku": "FD001", "category": "Food", "quantity": 100, "price": 5.5, "reorder_level": 10},
    {"name": "Wheat Flour", "sku": "FD002", "category": "Food", "quantity": 80, "price": 4.2, "reorder_level": 10},
    {"name": "Sugar", "sku": "FD003", "category": "Food", "quantity": 60, "price": 3.0, "reorder_level": 10},
    {"name": "Salt", "sku": "FD004", "category": "Food", "quantity": 40, "price": 1.5, "reorder_level": 10},
    {"name": "Milk", "sku": "FD005", "category": "Dairy", "quantity": 5, "price": 2.5, "reorder_level": 10},
    {"name": "Butter", "sku": "FD006", "category": "Dairy", "quantity": 15, "price": 4.5, "reorder_level": 5},
    {"name": "Cheese", "sku": "FD007", "category": "Dairy", "quantity": 8, "price": 6.0, "reorder_level": 10},
    {"name": "Eggs", "sku": "FD008", "category": "Dairy", "quantity": 50, "price": 0.2, "reorder_level": 12},

    {"name": "Coca Cola", "sku": "BV001", "category": "Beverage", "quantity": 45, "price": 2.5, "reorder_level": 10},
    {"name": "Pepsi", "sku": "BV002", "category": "Beverage", "quantity": 30, "price": 2.3, "reorder_level": 10},
    {"name": "Sprite", "sku": "BV003", "category": "Beverage", "quantity": 20, "price": 2.2, "reorder_level": 10},
    {"name": "Orange Juice", "sku": "BV004", "category": "Beverage", "quantity": 10, "price": 3.5, "reorder_level": 8},
    {"name": "Water Bottle", "sku": "BV005", "category": "Beverage", "quantity": 100, "price": 1.0, "reorder_level": 15},

    {"name": "Soap", "sku": "HC001", "category": "Household", "quantity": 40, "price": 2.0, "reorder_level": 10},
    {"name": "Shampoo", "sku": "HC002", "category": "Household", "quantity": 25, "price": 5.0, "reorder_level": 8},
    {"name": "Toothpaste", "sku": "HC003", "category": "Household", "quantity": 15, "price": 3.0, "reorder_level": 5},
    {"name": "Detergent", "sku": "HC004", "category": "Household", "quantity": 20, "price": 7.0, "reorder_level": 6},
    {"name": "Dish Soap", "sku": "HC005", "category": "Household", "quantity": 5, "price": 4.0, "reorder_level": 7},

    {"name": "Notebook", "sku": "ST001", "category": "Stationery", "quantity": 60, "price": 2.0, "reorder_level": 10},
    {"name": "Pen", "sku": "ST002", "category": "Stationery", "quantity": 100, "price": 1.0, "reorder_level": 20},
    {"name": "Pencil", "sku": "ST003", "category": "Stationery", "quantity": 80, "price": 0.5, "reorder_level": 20},
    {"name": "Marker", "sku": "ST004", "category": "Stationery", "quantity": 12, "price": 2.5, "reorder_level": 10},

    {"name": "Paracetamol", "sku": "MD001", "category": "Medicine", "quantity": 50, "price": 1.5, "reorder_level": 10},
    {"name": "Vitamin C", "sku": "MD002", "category": "Medicine", "quantity": 30, "price": 3.0, "reorder_level": 8},
    {"name": "Cough Syrup", "sku": "MD003", "category": "Medicine", "quantity": 10, "price": 6.0, "reorder_level": 10},
    {"name": "Bandages", "sku": "MD004", "category": "Medicine", "quantity": 25, "price": 2.0, "reorder_level": 5},

    {"name": "Bread", "sku": "BK001", "category": "Bakery", "quantity": 20, "price": 2.5, "reorder_level": 5},
    {"name": "Croissant", "sku": "BK002", "category": "Bakery", "quantity": 8, "price": 3.0, "reorder_level": 5},
    {"name": "Cookies", "sku": "BK003", "category": "Bakery", "quantity": 30, "price": 4.0, "reorder_level": 8},

    {"name": "Potato Chips", "sku": "SN001", "category": "Snacks", "quantity": 45, "price": 2.0, "reorder_level": 10},
    {"name": "Chocolate", "sku": "SN002", "category": "Snacks", "quantity": 50, "price": 1.8, "reorder_level": 12},
    {"name": "Biscuits", "sku": "SN003", "category": "Snacks", "quantity": 35, "price": 2.2, "reorder_level": 8},

    {"name": "Tomatoes", "sku": "VG001", "category": "Vegetables", "quantity": 25, "price": 2.5, "reorder_level": 8},
    {"name": "Onions", "sku": "VG002", "category": "Vegetables", "quantity": 35, "price": 1.8, "reorder_level": 10},
    {"name": "Potatoes", "sku": "VG003", "category": "Vegetables", "quantity": 60, "price": 2.0, "reorder_level": 10},
    {"name": "Carrots", "sku": "VG004", "category": "Vegetables", "quantity": 18, "price": 2.2, "reorder_level": 6},

    {"name": "Apple", "sku": "FR001", "category": "Fruits", "quantity": 40, "price": 3.0, "reorder_level": 10},
    {"name": "Banana", "sku": "FR002", "category": "Fruits", "quantity": 50, "price": 1.5, "reorder_level": 10},
    {"name": "Orange", "sku": "FR003", "category": "Fruits", "quantity": 30, "price": 2.5, "reorder_level": 8},
    {"name": "Mango", "sku": "FR004", "category": "Fruits", "quantity": 12, "price": 4.5, "reorder_level": 5},
]

for item in products:

    existing_product = db.query(Product).filter(
        Product.sku == item["sku"]
    ).first()

    if not existing_product:
        product = Product(**item)
        db.add(product)

db.commit()

print("Products seeded successfully!")
