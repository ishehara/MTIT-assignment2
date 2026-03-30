import os
from typing import Optional

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "computer_repair_management")
CUSTOMER_COLLECTION = os.getenv("CUSTOMER_COLLECTION", "customers")
INVENTORY_COLLECTION = os.getenv("INVENTORY_COLLECTION", "inventory_items")

_client = None


def _get_client():
    global _client
    if _client is None and MONGODB_URI:
        try:
            _client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        except Exception:
            _client = None
    return _client


def get_database():
    client = _get_client()
    if not client:
        return None
    return client[MONGODB_DB_NAME]


def get_collection(name: str) -> Optional[Collection]:
    db = get_database()
    if db is None:
        return None
    return db[name]


def check_mongo_connection() -> bool:
    client = _get_client()
    if not client:
        return False
    try:
        client.admin.command("ping")
        return True
    except PyMongoError:
        return False


def get_customer_collection() -> Optional[Collection]:
    return get_collection(CUSTOMER_COLLECTION)


def get_inventory_collection() -> Optional[Collection]:
    return get_collection(INVENTORY_COLLECTION)
