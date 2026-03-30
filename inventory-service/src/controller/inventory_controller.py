from typing import Annotated, Any, List

from fastapi import APIRouter, Depends, Response, status

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


@router.post("/inventory", response_model=InventoryResponseDTO, status_code=status.HTTP_201_CREATED)
def create_item(payload: InventoryCreateDTO, collection: CollectionDep):
    service = InventoryService(collection)
    item = service.create_item(payload)
    return InventoryResponseDTO.model_validate(item)


@router.get("/inventory", response_model=List[InventoryResponseDTO], status_code=status.HTTP_200_OK)
def get_all_items(collection: CollectionDep):
    service = InventoryService(collection)
    items = service.get_all_items()
    return [InventoryResponseDTO.model_validate(item) for item in items]


@router.get("/inventory/{item_id}", response_model=InventoryResponseDTO, status_code=status.HTTP_200_OK)
def get_item_by_id(item_id: str, collection: CollectionDep):
    service = InventoryService(collection)
    item = service.get_item_by_id(item_id)
    return InventoryResponseDTO.model_validate(item)


@router.put("/inventory/{item_id}", response_model=InventoryResponseDTO, status_code=status.HTTP_200_OK)
def update_item(item_id: str, payload: InventoryUpdateDTO, collection: CollectionDep):
    service = InventoryService(collection)
    item = service.update_item(item_id, payload)
    return InventoryResponseDTO.model_validate(item)


@router.delete("/inventory/{item_id}", response_model=MessageResponseDTO, status_code=status.HTTP_200_OK)
def delete_item(item_id: str, collection: CollectionDep):
    service = InventoryService(collection)
    service.delete_item(item_id)
    return MessageResponseDTO(message=f"Inventory item with ID {item_id} deleted successfully", status="success")
