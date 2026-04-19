from typing import Annotated, Any, List

from fastapi import APIRouter, Depends, Path, Response, status

from src.config.database import get_inventory_collection
from src.dto.inventory_dto import (
    InventoryCreateDTO,
    InventoryResponseDTO,
    InventoryUpdateDTO,
    MessageResponseDTO,
)
from src.service.inventory_service import InventoryService

router = APIRouter(tags=["Inventory"])
CollectionDep = Annotated[Any, Depends(get_inventory_collection)]


@router.post(
    "/inventory",
    response_model=InventoryResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new inventory item",
    description="Create a new inventory item with validation checks",
)
def create_item(payload: InventoryCreateDTO, collection: CollectionDep):
    """Create a new inventory item."""
    service = InventoryService(collection)
    item = service.create_item(payload)
    return InventoryResponseDTO.model_validate(item)


@router.get(
    "/inventory",
    response_model=List[InventoryResponseDTO],
    status_code=status.HTTP_200_OK,
    summary="Get all inventory items",
    description="Retrieve all inventory items from the system",
)
def get_all_items(collection: CollectionDep):
    """Get all inventory items."""
    service = InventoryService(collection)
    items = service.get_all_items()
    return [InventoryResponseDTO.model_validate(item) for item in items]


@router.get(
    "/inventory/{item_id}",
    response_model=InventoryResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Get inventory item by ID",
    description="Retrieve a specific inventory item by its ID",
)
def get_item_by_id(
    item_id: str = Path(..., min_length=24, max_length=24, description="The inventory item ID"),
    collection: CollectionDep = None,
):
    """Get inventory item by ID with validation."""
    service = InventoryService(collection)
    item = service.get_item_by_id(item_id)
    return InventoryResponseDTO.model_validate(item)


@router.put(
    "/inventory/{item_id}",
    response_model=InventoryResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Update an inventory item",
    description="Update an existing inventory item with validation checks",
)
def update_item(
    item_id: str = Path(..., min_length=24, max_length=24, description="The inventory item ID"),
    payload: InventoryUpdateDTO = None,
    collection: CollectionDep = None,
):
    """Update an inventory item with validation."""
    service = InventoryService(collection)
    item = service.update_item(item_id, payload)
    return InventoryResponseDTO.model_validate(item)


@router.delete(
    "/inventory/{item_id}",
    response_model=MessageResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Delete an inventory item",
    description="Delete an existing inventory item by its ID",
)
def delete_item(
    item_id: str = Path(..., min_length=24, max_length=24, description="The inventory item ID"),
    collection: CollectionDep = None,
):
    """Delete an inventory item with validation."""
    service = InventoryService(collection)
    service.delete_item(item_id)
    return MessageResponseDTO(message=f"Inventory item with ID {item_id} deleted successfully", status="success")
