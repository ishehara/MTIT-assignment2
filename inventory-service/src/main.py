from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config.database import check_mongo_connection, get_inventory_collection
from src.config.settings import settings
from src.controller.inventory_controller import router as inventory_router
from src.data.seed_data import seed_inventory_items
from src.middleware.exception_handler import register_exception_handlers


@asynccontextmanager
async def lifespan(_: FastAPI):
    collection = get_inventory_collection()
    if collection is not None:
        seed_inventory_items(collection)

    yield


app = FastAPI(
    title="Inventory Management Service",
    version=settings.APP_VERSION,
    description="Inventory microservice for university microservices architecture",
    lifespan=lifespan,
)

app.include_router(inventory_router)
app.include_router(inventory_router, prefix="/api")


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "UP",
        "service": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "database": "UP" if check_mongo_connection() else "DOWN",
    }


register_exception_handlers(app)
