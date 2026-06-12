from fastapi import FastAPI
from app.api.routes.product import router as product_router
from app.api.routes.customer import (
    router as customer_router
)
from app.api.routes.sale import (
    router as sale_router
)

app = FastAPI(
    title="Micro ERP AI",
    version="0.1.0"
)

app.include_router(product_router)
app.include_router(customer_router)
app.include_router(sale_router)


@app.get("/")
def home():
    return {
        "message": "Micro ERP API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }