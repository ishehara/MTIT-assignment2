import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME = os.getenv("APP_NAME", "inventory-service")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    APP_ENV = os.getenv("APP_ENV", "development")
    APP_HOST = os.getenv("APP_HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", "8003"))

    MONGODB_URI = os.getenv("MONGODB_URI", "")
    MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "ComputerRepairManagementSystem")
    INVENTORY_COLLECTION = os.getenv("INVENTORY_COLLECTION", "inventory_items")


settings = Settings()
