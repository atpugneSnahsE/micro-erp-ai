from fastapi import FastAPI
from app.api.routes.product import router as product_router
from app.api.routes.customer import (
    router as customer_router
)
from app.api.routes.sale import (
    router as sale_router
)
from app.api.routes.dashboard import (
    router as dashboard_router
)
from app.api.routes.auth import (
    router as auth_router
)
from app.api.routes.report import (
    router as report_router
)

app = FastAPI(
    title="Micro ERP AI",
    version="0.1.0"
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(
    product_router,
    prefix="/api/v1",
    tags=["Products"]
)

app.include_router(
    customer_router,
    prefix="/api/v1",
    tags=["Customers"]
)

app.include_router(
    dashboard_router,
    prefix="/api/v1",
    tags=["Dashboard"]
)

app.include_router(
    sale_router,
    prefix="/api/v1",
    tags=["Sales"]
)

app.include_router(
    dashboard_router,
    prefix="/api/v1",
    tags=["Dashboard"]
)

app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

app.include_router(
    report_router,
    prefix="/api/v1",
    tags=["Reports"]
)

@app.get("/")
def home():
    return {
        "message": "Micro ERP API is running"
    }
