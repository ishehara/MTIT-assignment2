from typing import Any, Dict, List

from src.dto.repair_dto import RepairJobCreateDTO, RepairJobUpdateDTO, RepairJobUpdateStatusDTO
from src.errors.exceptions import BadRequestException, NotFoundException
from src.repository.repair_repository import RepairRepository


class RepairService:
    def __init__(self, collection):
        self.repository = RepairRepository(collection)

    def register_device(self, payload: RepairJobCreateDTO) -> Dict[str, Any]:
        return self.repository.create(payload.model_dump())

    def get_all_jobs(self) -> List[Dict[str, Any]]:
        return self.repository.find_all()

    def get_job_by_id(self, job_id: str) -> Dict[str, Any]:
        job = self.repository.find_by_id(job_id)
        if not job:
            raise NotFoundException(f"Repair job with id '{job_id}' not found")
        return job

    def get_jobs_by_status(self, status: str) -> List[Dict[str, Any]]:
        return self.repository.find_by_status(status)

    def update_status(self, job_id: str, payload: RepairJobUpdateStatusDTO) -> Dict[str, Any]:
        self.get_job_by_id(job_id)
        update_data = {}
        if payload.status is not None:
            update_data["status"] = payload.status.value
        if payload.technician_notes is not None:
            update_data["technician_notes"] = payload.technician_notes
        if not update_data:
            raise BadRequestException("No fields provided to update")
        updated = self.repository.update_status(job_id, update_data)
        if not updated:
            raise NotFoundException(f"Repair job with id '{job_id}' not found")
        return updated

    def update_job(self, job_id: str, payload: RepairJobUpdateDTO) -> Dict[str, Any]:
        self.get_job_by_id(job_id)
        update_data = payload.model_dump(exclude_unset=True)
        if not update_data:
            raise BadRequestException("No fields provided to update")
        updated = self.repository.update(job_id, update_data)
        if not updated:
            raise NotFoundException(f"Repair job with id '{job_id}' not found")
        return updated

    def delete_job(self, job_id: str) -> None:
        self.get_job_by_id(job_id)
        self.repository.delete(job_id)
