import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME = os.getenv("GATEWAY_APP_NAME", "API Gateway")
    APP_VERSION = os.getenv("GATEWAY_APP_VERSION", "2.0.0")
    APP_ENV = os.getenv("APP_ENV", "development")
    APP_HOST = os.getenv("APP_HOST", "127.0.0.1")
    APP_PORT = int(os.getenv("APP_PORT", "8000"))

    # Shared MongoDB configuration for services.
    MONGODB_URI = os.getenv("MONGODB_URI", "")
    MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "ComputerRepairManagementSystem")

    INVENTORY_SERVICE_URL = os.getenv("INVENTORY_SERVICE_URL", "http://localhost:8003")
    REPAIR_SERVICE_URL = os.getenv("REPAIR_SERVICE_URL", "http://localhost:8004")
    STAFF_SERVICE_URL = os.getenv("STAFF_SERVICE_URL", "http://localhost:8005")


settings = Settings()
