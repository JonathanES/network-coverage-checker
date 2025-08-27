from fastapi import FastAPI
from src.api.urls import router

app = FastAPI(title="Network Coverage API", version="1.0.0")

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
