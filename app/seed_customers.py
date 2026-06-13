from app.database import SessionLocal
from app.models.customer import Customer

db = SessionLocal()

customers = [
    {
        "name": "Johnny Doe",
        "phone": "9874543210",
        "email": "johnyn@email.com",
        "address": "New York",
        "credit_balance": 0
    },
    {
        "name": "Sarah Smith",
        "phone": "9988776655",
        "email": "sarah@email.com",
        "address": "Chicago",
        "credit_balance": 100
    },
    {
        "name": "Michael Brown",
        "phone": "9911223344",
        "email": "michael@email.com",
        "address": "California",
        "credit_balance": 50
    },
    {
        "name": "Emma Wilson",
        "phone": "9988123456",
        "email": "emma@email.com",
        "address": "Texas",
        "credit_balance": 0
    }
]

for item in customers:

    existing_customer = db.query(Customer).filter(
        Customer.email == item["email"]
    ).first()

    if not existing_customer:
        customer = Customer(**item)
        db.add(customer)

db.commit()

print("Customers seeded successfully!")
