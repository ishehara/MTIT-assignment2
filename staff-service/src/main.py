from contextlib import asynccontextmanager

from fastapi import FastAPI

from .config.database import check_mongo_connection, get_staff_collection
from .config.settings import settings
from .controller.staff_controller import router as staff_router
from .data.seed_data import seed_staff_data
from .middleware.exception_handler import register_exception_handlers


@asynccontextmanager
async def lifespan(_: FastAPI):
    collection = get_staff_collection()
    if collection is not None:
        seed_staff_data(collection)

    yield


app = FastAPI(
    title="Staff Management Service",
    version=settings.APP_VERSION,
    description="Staff microservice for Computer Repair Management System",
    lifespan=lifespan,
)


app.include_router(staff_router, prefix="/api")


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "UP",
        "service": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "database": "UP" if check_mongo_connection() else "DOWN",
    }


register_exception_handlers(app)
