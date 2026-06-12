from fastapi import FastAPI

app = FastAPI(
    title="Micro ERP AI",
    version="0.1.0"
)

@app.get("/")
def home():
    return {"message": "Micro ERP API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}