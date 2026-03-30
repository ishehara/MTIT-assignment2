from typing import Any, Dict, List

from ..dto.staff_dto import StaffCreateRequest, StaffUpdateRequest
from ..errors.exceptions import NotFoundException
from ..repository.staff_repository import StaffRepository


class StaffService:
    def __init__(self, collection):
        self.repository = StaffRepository(collection)

    def create_staff(self, payload: StaffCreateRequest) -> Dict[str, Any]:
        return self.repository.create(payload.model_dump())

    def get_all_staff(self) -> List[Dict[str, Any]]:
        return self.repository.find_all()

    def get_staff_by_id(self, staff_id: str) -> Dict[str, Any]:
        staff = self.repository.find_by_id(staff_id)
        if not staff:
            raise NotFoundException(f"Staff member with id {staff_id} not found")
        return staff

    def update_staff(self, staff_id: str, payload: StaffUpdateRequest) -> Dict[str, Any]:
        self.get_staff_by_id(staff_id)
        update_data = payload.model_dump(exclude_unset=True)
        updated_staff = self.repository.update(staff_id, update_data)
        if not updated_staff:
            raise NotFoundException(f"Staff member with id {staff_id} not found")
        return updated_staff

    def delete_staff(self, staff_id: str) -> None:
        self.get_staff_by_id(staff_id)
        self.repository.delete(staff_id)
