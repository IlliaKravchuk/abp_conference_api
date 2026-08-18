from fastapi import FastAPI
from app.api.endpoints import router as api_router
from app.infrastructure.database import engine, Base

# Створення таблиць дляБД
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ABP Conference Booking API",
    description="API для управління залами, бронюваннями та розрахунку вартості оренди.",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")