from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import ServerSelectionTimeoutError

from .settings import settings

_client: MongoClient | None = None
_db = None


def get_mongo_client() -> MongoClient | None:
    global _client
    try:
        if _client is None:
            _client = MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=5000)
        return _client
    except ServerSelectionTimeoutError:
        return None


def get_database():
    global _db
    if _db is None:
        client = get_mongo_client()
        if client:
            _db = client[settings.MONGODB_DB_NAME]
    return _db


def get_staff_collection() -> Collection | None:
    db = get_database()
    if db is not None:
        return db[settings.STAFF_COLLECTION]
    return None


def check_mongo_connection() -> bool:
    try:
        client = get_mongo_client()
        if client:
            client.admin.command("ping")
            return True
    except Exception:
        pass
    return False
