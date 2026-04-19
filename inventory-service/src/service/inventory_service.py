from typing import Any, Dict, List

from src.dto.inventory_dto import InventoryCreateDTO, InventoryUpdateDTO
from src.errors.exceptions import NotFoundException, ValidationException, BadRequestException
from src.repository.inventory_repository import InventoryRepository


class InventoryService:
    def __init__(self, collection):
        self.repository = InventoryRepository(collection)

    def _validate_item_id(self, item_id: str) -> None:
        """Validate that item_id is not empty and is a valid format."""
        if not item_id or not item_id.strip():
            raise BadRequestException("Item ID cannot be empty")
        if len(item_id) != 24:
            raise BadRequestException("Invalid item ID format")

    def create_item(self, payload: InventoryCreateDTO) -> Dict[str, Any]:
        """Create a new inventory item with validation."""
        # Payload validation is handled by Pydantic DTO
        try:
            return self.repository.create(payload.model_dump())
        except Exception as e:
            raise ValidationException(f"Failed to create inventory item: {str(e)}")

    def get_all_items(self) -> List[Dict[str, Any]]:
        """Retrieve all inventory items."""
        try:
            return self.repository.find_all()
        except Exception as e:
            raise ValidationException(f"Failed to retrieve inventory items: {str(e)}")

    def get_item_by_id(self, item_id: str) -> Dict[str, Any]:
        """Retrieve inventory item by ID with validation."""
        self._validate_item_id(item_id)
        item = self.repository.find_by_id(item_id)
        if not item:
            raise NotFoundException(f"Inventory item with id {item_id} not found")
        return item

    def update_item(self, item_id: str, payload: InventoryUpdateDTO) -> Dict[str, Any]:
        """Update inventory item with validation."""
        self._validate_item_id(item_id)
        
        # Verify item exists
        self.get_item_by_id(item_id)
        
        # Prepare update data (exclude unset fields)
        update_data = payload.model_dump(exclude_unset=True)
        
        if not update_data:
            raise BadRequestException("No fields provided for update")
        
        try:
            updated_item = self.repository.update(item_id, update_data)
            if not updated_item:
                raise NotFoundException(f"Inventory item with id {item_id} not found")
            return updated_item
        except Exception as e:
            raise ValidationException(f"Failed to update inventory item: {str(e)}")

    def delete_item(self, item_id: str) -> None:
        """Delete inventory item with validation."""
        self._validate_item_id(item_id)
        self.get_item_by_id(item_id)
        try:
            self.repository.delete(item_id)
        except Exception as e:
            raise ValidationException(f"Failed to delete inventory item: {str(e)}")
