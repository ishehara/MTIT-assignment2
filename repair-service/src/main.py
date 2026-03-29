from fastapi import FastAPI

from src.config.database import check_mongo_connection
from src.config.settings import settings
from src.controller.repair_controller import router as repair_router
from src.middleware.exception_handler import register_exception_handlers

app = FastAPI(
    title="Repair Service",
    version=settings.APP_VERSION,
    description="Microservice for managing device repair jobs — registration, status tracking, and handover.",
)

app.include_router(repair_router)
app.include_router(repair_router, prefix="/api")


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "UP",
        "service": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "database": "UP" if check_mongo_connection() else "DOWN",
    }


register_exception_handlers(app)
