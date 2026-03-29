from pymongo import MongoClient
from pymongo.errors import PyMongoError

from src.config.settings import settings

client = MongoClient(settings.MONGODB_URI) if settings.MONGODB_URI else None


def get_database():
    if not client:
        return None
    return client[settings.MONGODB_DB_NAME]


def get_inventory_collection():
    db = get_database()
    if db is None:
        return None
    return db[settings.INVENTORY_COLLECTION]


def check_mongo_connection() -> bool:
    if not client:
        return False
    try:
        client.admin.command("ping")
        return True
    except PyMongoError:
        return False
