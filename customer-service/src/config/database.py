from typing import Optional

import certifi
from pymongo import ASCENDING, MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

from src.config.settings import settings

client = (
    MongoClient(settings.MONGODB_URI, tlsCAFile=certifi.where())
    if settings.MONGODB_URI
    else None
)


def get_database():
    if not client:
        return None
    return client[settings.MONGODB_DB_NAME]


def get_customer_collection() -> Optional[Collection]:
    db = get_database()
    if db is None:
        return None
    return db[settings.CUSTOMER_COLLECTION]


def ensure_customer_indexes(collection: Collection) -> None:
    try:
        collection.create_index(
            [("customerId", ASCENDING)],
            unique=True,
            name="customer_id_unique_index",
        )
    except PyMongoError:
        pass


def check_mongo_connection() -> bool:
    if not client:
        return False
    try:
        client.admin.command("ping")
        return True
    except PyMongoError:
        return False
