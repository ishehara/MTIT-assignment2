from pymongo import MongoClient
from pymongo.errors import PyMongoError

from src.config.settings import settings

_client = None


def _get_client():
    global _client
    if _client is None and settings.MONGODB_URI:
        try:
            _client = MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=5000)
        except Exception:
            _client = None
    return _client


def get_database():
    client = _get_client()
    if not client:
        return None
    return client[settings.MONGODB_DB_NAME]


def get_repairs_collection():
    db = get_database()
    if db is None:
        return None
    return db[settings.REPAIRS_COLLECTION]


def check_mongo_connection() -> bool:
    client = _get_client()
    if not client:
        return False
    try:
        client.admin.command("ping")
        return True
    except PyMongoError:
        return False
