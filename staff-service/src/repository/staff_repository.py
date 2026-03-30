from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from bson import ObjectId
from pymongo.collection import Collection


class StaffRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    @staticmethod
    def _to_response_doc(document: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "id": str(document["_id"]),
            "name": document["name"],
            "email": document.get("email"),
            "phone": document["phone"],
            "specialty": document["specialty"],
            "workload": document["workload"],
            "status": document["status"],
            "created_at": document["created_at"],
        }

    def create(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        payload["workload"] = 0
        payload["created_at"] = datetime.now(timezone.utc)
        insert_result = self.collection.insert_one(payload)
        document = self.collection.find_one({"_id": insert_result.inserted_id})
        return self._to_response_doc(document)

    def find_all(self) -> List[Dict[str, Any]]:
        documents = self.collection.find().sort("created_at", -1)
        return [self._to_response_doc(doc) for doc in documents]

    def find_by_id(self, staff_id: str) -> Optional[Dict[str, Any]]:
        if not ObjectId.is_valid(staff_id):
            return None
        document = self.collection.find_one({"_id": ObjectId(staff_id)})
        if not document:
            return None
        return self._to_response_doc(document)

    def update(self, staff_id: str, update_payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not ObjectId.is_valid(staff_id):
            return None

        self.collection.update_one(
            {"_id": ObjectId(staff_id)},
            {"$set": update_payload},
        )
        document = self.collection.find_one({"_id": ObjectId(staff_id)})
        if not document:
            return None
        return self._to_response_doc(document)

    def delete(self, staff_id: str) -> bool:
        if not ObjectId.is_valid(staff_id):
            return False
        result = self.collection.delete_one({"_id": ObjectId(staff_id)})
        return result.deleted_count > 0

    def count(self) -> int:
        return self.collection.count_documents({})
