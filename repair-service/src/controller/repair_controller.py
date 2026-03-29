from typing import Annotated, Any, List

from fastapi import APIRouter, Depends, Response, status

from src.config.database import get_repairs_collection
from src.dto.repair_dto import (
    RepairJobCreateDTO,
    RepairJobResponseDTO,
    RepairJobUpdateDTO,
    RepairJobUpdateStatusDTO,
    RepairStatus,
)
from src.service.repair_service import RepairService

router = APIRouter(tags=["Repair Jobs"])
CollectionDep = Annotated[Any, Depends(get_repairs_collection)]


@router.post(
    "/repairs",
    response_model=RepairJobResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new device for repair",
)
def register_device(payload: RepairJobCreateDTO, collection: CollectionDep):
    service = RepairService(collection)
    job = service.register_device(payload)
    return RepairJobResponseDTO.model_validate(job)


@router.get(
    "/repairs",
    response_model=List[RepairJobResponseDTO],
    status_code=status.HTTP_200_OK,
    summary="List all repair jobs",
)
def get_all_jobs(collection: CollectionDep):
    service = RepairService(collection)
    jobs = service.get_all_jobs()
    return [RepairJobResponseDTO.model_validate(job) for job in jobs]


@router.get(
    "/repairs/status/{status}",
    response_model=List[RepairJobResponseDTO],
    status_code=status.HTTP_200_OK,
    summary="Filter repair jobs by status",
)
def get_jobs_by_status(status: RepairStatus, collection: CollectionDep):
    service = RepairService(collection)
    jobs = service.get_jobs_by_status(status.value)
    return [RepairJobResponseDTO.model_validate(job) for job in jobs]


@router.get(
    "/repairs/{job_id}",
    response_model=RepairJobResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Get a repair job by ID",
)
def get_job_by_id(job_id: str, collection: CollectionDep):
    service = RepairService(collection)
    job = service.get_job_by_id(job_id)
    return RepairJobResponseDTO.model_validate(job)


@router.patch(
    "/repairs/{job_id}/status",
    response_model=RepairJobResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Update repair status and/or technician notes",
)
def update_repair_status(job_id: str, payload: RepairJobUpdateStatusDTO, collection: CollectionDep):
    service = RepairService(collection)
    job = service.update_status(job_id, payload)
    return RepairJobResponseDTO.model_validate(job)


@router.put(
    "/repairs/{job_id}",
    response_model=RepairJobResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Update customer or device details of a repair job",
)
def update_repair_job(job_id: str, payload: RepairJobUpdateDTO, collection: CollectionDep):
    service = RepairService(collection)
    job = service.update_job(job_id, payload)
    return RepairJobResponseDTO.model_validate(job)


@router.delete(
    "/repairs/{job_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a repair job record",
)
def delete_job(job_id: str, collection: CollectionDep):
    service = RepairService(collection)
    service.delete_job(job_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
