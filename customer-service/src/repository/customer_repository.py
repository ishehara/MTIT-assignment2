from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pymongo.collection import Collection


class CustomerRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    @staticmethod
    def _normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "id": str(document["_id"]),
            "customer_id": document["customerId"],
            "name": document["name"],
            "phone": document["phone"],
            "email": document["email"],
            "address": document["address"],
            "device_type": document["deviceType"],
            "device_issue": document["deviceIssue"],
            "device_status": document["deviceStatus"],
            "repair_history": document.get("repairHistory", []),
            "createdAt": document["createdAt"],
            "updatedAt": document["updatedAt"],
        }

    @staticmethod
    def _prepare_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
        data = payload.copy()
        data["customerId"] = data.pop("customer_id")
        data["deviceType"] = data.pop("device_type")
        data["deviceIssue"] = data.pop("device_issue")
        data["deviceStatus"] = data.pop("device_status")
        data["repairHistory"] = data.get("repair_history", [])
        data.pop("repair_history", None)
        return data

    def create(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        data = self._prepare_payload(payload)
        data["createdAt"] = now
        data["updatedAt"] = now
        insert_result = self.collection.insert_one(data)
        document = self.collection.find_one({"_id": insert_result.inserted_id})
        return self._normalize_document(document)

    def find_all(self) -> List[Dict[str, Any]]:
        documents = self.collection.find().sort("createdAt", -1)
        return [self._normalize_document(doc) for doc in documents]

    def find_by_customer_id(self, customer_id: int) -> Optional[Dict[str, Any]]:
        document = self.collection.find_one({"customerId": customer_id})
        if not document:
            return None
        return self._normalize_document(document)

    def update_by_customer_id(self, customer_id: int, update_payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        update_data = update_payload.copy()
        if "customer_id" in update_data:
            update_data.pop("customer_id")
        if "device_type" in update_data:
            update_data["deviceType"] = update_data.pop("device_type")
        if "device_issue" in update_data:
            update_data["deviceIssue"] = update_data.pop("device_issue")
        if "device_status" in update_data:
            update_data["deviceStatus"] = update_data.pop("device_status")
        if "repair_history" in update_data:
            update_data["repairHistory"] = update_data.pop("repair_history")
        update_data["updatedAt"] = datetime.now(timezone.utc)

        result = self.collection.update_one(
            {"customerId": customer_id},
            {"$set": update_data},
        )
        if result.matched_count == 0:
            return None
        document = self.collection.find_one({"customerId": customer_id})
        if not document:
            return None
        return self._normalize_document(document)

    def delete_by_customer_id(self, customer_id: int) -> bool:
        result = self.collection.delete_one({"customerId": customer_id})
        return result.deleted_count > 0

    def exists_by_customer_id(self, customer_id: int) -> bool:
        return self.collection.count_documents({"customerId": customer_id}, limit=1) > 0
