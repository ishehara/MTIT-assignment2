from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config.database import (
    check_mongo_connection,
    ensure_customer_indexes,
    get_customer_collection,
)
from src.config.settings import settings
from src.controller.customer_controller import router as customer_router
from src.middleware.exception_handler import register_exception_handlers


@asynccontextmanager
async def lifespan(_: FastAPI):
    collection = get_customer_collection()
    if collection is not None:
        ensure_customer_indexes(collection)
    yield


app = FastAPI(
    title="Customer Service",
    version=settings.APP_VERSION,
    description="Customer microservice for managing contact info and repair history",
    lifespan=lifespan,
)

app.include_router(customer_router)
app.include_router(customer_router, prefix="/api")


@app.get("/", tags=["Info"])
def read_root():
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "Customer microservice",
        "database": "UP" if check_mongo_connection() else "DOWN",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "UP",
        "service": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "database": "UP" if check_mongo_connection() else "DOWN",
    }


register_exception_handlers(app)
