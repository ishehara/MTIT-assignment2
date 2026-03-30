import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME = os.getenv("CUSTOMER_APP_NAME", "customer-service")
    APP_VERSION = os.getenv("CUSTOMER_APP_VERSION", "1.0.0")
    APP_ENV = os.getenv("APP_ENV", "development")
    APP_HOST = os.getenv("APP_HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", "8002"))

    MONGODB_URI = os.getenv("MONGODB_URI", "")
    MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "ComputerRepairManagementSystem")
    CUSTOMER_COLLECTION = os.getenv("CUSTOMER_COLLECTION", "customers")


settings = Settings()
