from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from bson import ObjectId
from pymongo.collection import Collection


class InventoryRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    @staticmethod
    def _to_response_doc(document: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "id": str(document["_id"]),
            "name": document["name"],
            "description": document["description"],
            "quantity": document["quantity"],
            "price": document["price"],
            "supplier": document.get("supplier", "Unknown"),
            "condition": document.get("condition", "Unknown"),
            "warranty_period": document.get("warranty_period", "None"),
            "createdAt": document["createdAt"],
        }

    def create(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        payload["createdAt"] = datetime.now(timezone.utc)
        insert_result = self.collection.insert_one(payload)
        document = self.collection.find_one({"_id": insert_result.inserted_id})
        return self._to_response_doc(document)

    def find_all(self) -> List[Dict[str, Any]]:
        documents = self.collection.find().sort("createdAt", -1)
        return [self._to_response_doc(doc) for doc in documents]

    def find_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        if not ObjectId.is_valid(item_id):
            return None
        document = self.collection.find_one({"_id": ObjectId(item_id)})
        if not document:
            return None
        return self._to_response_doc(document)

    def update(self, item_id: str, update_payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not ObjectId.is_valid(item_id):
            return None

        self.collection.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": update_payload},
        )
        document = self.collection.find_one({"_id": ObjectId(item_id)})
        if not document:
            return None
        return self._to_response_doc(document)

    def delete(self, item_id: str) -> bool:
        if not ObjectId.is_valid(item_id):
            return False
        result = self.collection.delete_one({"_id": ObjectId(item_id)})
        return result.deleted_count > 0

    def count(self) -> int:
        return self.collection.count_documents({})
