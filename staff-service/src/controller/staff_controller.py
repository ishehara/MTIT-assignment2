from typing import Annotated, Any, List

from fastapi import APIRouter, Depends, Response, status

from ..config.database import get_staff_collection
from ..dto.staff_dto import StaffCreateRequest, StaffUpdateRequest, StaffResponse
from ..service.staff_service import StaffService

router = APIRouter(tags=["Staff"])
CollectionDep = Annotated[Any, Depends(get_staff_collection)]


@router.post("/staff", response_model=StaffResponse, status_code=status.HTTP_201_CREATED)
def create_staff(payload: StaffCreateRequest, collection: CollectionDep):
    service = StaffService(collection)
    staff = service.create_staff(payload)
    return StaffResponse.model_validate(staff)


@router.get("/staff", response_model=List[StaffResponse], status_code=status.HTTP_200_OK)
def get_all_staff(collection: CollectionDep):
    service = StaffService(collection)
    staff_list = service.get_all_staff()
    return [StaffResponse.model_validate(staff) for staff in staff_list]


@router.get("/staff/{staff_id}", response_model=StaffResponse, status_code=status.HTTP_200_OK)
def get_staff_by_id(staff_id: str, collection: CollectionDep):
    service = StaffService(collection)
    staff = service.get_staff_by_id(staff_id)
    return StaffResponse.model_validate(staff)


@router.put("/staff/{staff_id}", response_model=StaffResponse, status_code=status.HTTP_200_OK)
def update_staff(staff_id: str, payload: StaffUpdateRequest, collection: CollectionDep):
    service = StaffService(collection)
    staff = service.update_staff(staff_id, payload)
    return StaffResponse.model_validate(staff)


@router.delete("/staff/{staff_id}", status_code=status.HTTP_200_OK)
def delete_staff(staff_id: str, collection: CollectionDep):
    service = StaffService(collection)
    service.delete_staff(staff_id)
    return {"message": f"Staff member with ID {staff_id} deleted successfully", "status": "success"}
