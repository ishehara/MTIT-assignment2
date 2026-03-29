from typing import Any, Dict, List

from src.dto.inventory_dto import InventoryCreateDTO, InventoryUpdateDTO
from src.errors.exceptions import NotFoundException
from src.repository.inventory_repository import InventoryRepository


class InventoryService:
    def __init__(self, collection):
        self.repository = InventoryRepository(collection)

    def create_item(self, payload: InventoryCreateDTO) -> Dict[str, Any]:
        return self.repository.create(payload.model_dump())

    def get_all_items(self) -> List[Dict[str, Any]]:
        return self.repository.find_all()

    def get_item_by_id(self, item_id: str) -> Dict[str, Any]:
        item = self.repository.find_by_id(item_id)
        if not item:
            raise NotFoundException(f"Inventory item with id {item_id} not found")
        return item

    def update_item(self, item_id: str, payload: InventoryUpdateDTO) -> Dict[str, Any]:
        self.get_item_by_id(item_id)
        update_data = payload.model_dump(exclude_unset=True)
        updated_item = self.repository.update(item_id, update_data)
        if not updated_item:
            raise NotFoundException(f"Inventory item with id {item_id} not found")
        return updated_item

    def delete_item(self, item_id: str) -> None:
        self.get_item_by_id(item_id)
        self.repository.delete(item_id)
