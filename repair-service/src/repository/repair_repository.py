from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from bson import ObjectId
from pymongo.collection import Collection

from src.dto.repair_dto import RepairStatus


class RepairRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    @staticmethod
    def _to_response_doc(document: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "id": str(document["_id"]),
            "customer_name": document["customer_name"],
            "customer_phone": document["customer_phone"],
            "customer_email": document.get("customer_email"),
            "device_type": document["device_type"],
            "device_brand": document["device_brand"],
            "device_model": document["device_model"],
            "issue_description": document["issue_description"],
            "status": document["status"],
            "technician_notes": document.get("technician_notes"),
            "created_at": document["created_at"],
            "updated_at": document["updated_at"],
        }

    def create(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        payload["status"] = RepairStatus.NOT_STARTED.value
        payload["technician_notes"] = None
        payload["created_at"] = now
        payload["updated_at"] = now
        result = self.collection.insert_one(payload)
        document = self.collection.find_one({"_id": result.inserted_id})
        return self._to_response_doc(document)

    def find_all(self) -> List[Dict[str, Any]]:
        documents = self.collection.find().sort("created_at", -1)
        return [self._to_response_doc(doc) for doc in documents]

    def find_by_id(self, job_id: str) -> Optional[Dict[str, Any]]:
        if not ObjectId.is_valid(job_id):
            return None
        document = self.collection.find_one({"_id": ObjectId(job_id)})
        if not document:
            return None
        return self._to_response_doc(document)

    def find_by_status(self, status: str) -> List[Dict[str, Any]]:
        documents = self.collection.find({"status": status}).sort("created_at", -1)
        return [self._to_response_doc(doc) for doc in documents]

    def update_status(self, job_id: str, update_payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not ObjectId.is_valid(job_id):
            return None
        update_payload["updated_at"] = datetime.now(timezone.utc)
        self.collection.update_one(
            {"_id": ObjectId(job_id)},
            {"$set": update_payload},
        )
        document = self.collection.find_one({"_id": ObjectId(job_id)})
        if not document:
            return None
        return self._to_response_doc(document)

    def update(self, job_id: str, update_payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not ObjectId.is_valid(job_id):
            return None
        update_payload["updated_at"] = datetime.now(timezone.utc)
        self.collection.update_one(
            {"_id": ObjectId(job_id)},
            {"$set": update_payload},
        )
        document = self.collection.find_one({"_id": ObjectId(job_id)})
        if not document:
            return None
        return self._to_response_doc(document)

    def delete(self, job_id: str) -> bool:
        if not ObjectId.is_valid(job_id):
            return False
        result = self.collection.delete_one({"_id": ObjectId(job_id)})
        return result.deleted_count > 0
