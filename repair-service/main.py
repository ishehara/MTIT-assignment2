import uvicorn

from src.config.settings import settings

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=settings.APP_HOST,
        port=settings.PORT,
        reload=settings.APP_ENV == "development",
    )


