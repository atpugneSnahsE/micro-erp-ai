from fastapi import FastAPI
from app.api.routes.product import router as product_router

app = FastAPI(
    title="Micro ERP AI",
    version="0.1.0"
)

app.include_router(product_router)


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