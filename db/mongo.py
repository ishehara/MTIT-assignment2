import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "computer_repair_management")

_client = MongoClient(MONGODB_URI) if MONGODB_URI else None


def get_database():
    if not _client:
        return None
    return _client[MONGODB_DB_NAME]


def check_mongo_connection() -> bool:
    if not _client:
        return False
    try:
        _client.admin.command("ping")
        return True
    except PyMongoError:
        return False
