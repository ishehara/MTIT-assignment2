from typing import Annotated, Any, List

from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.config.database import get_customer_collection
from src.dto.customer_dto import (
    CustomerCreateDTO,
    CustomerResponseDTO,
    CustomerUpdateDTO,
)
from src.service.customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["Customers"])
CollectionDep = Annotated[Any, Depends(get_customer_collection)]


def _build_service(collection: Any) -> CustomerService:
    if collection is None:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable. Ensure MongoDB is running and configured.",
        )
    return CustomerService(collection)


@router.post("", response_model=CustomerResponseDTO, status_code=status.HTTP_201_CREATED)
def create_customer(payload: CustomerCreateDTO, collection: CollectionDep):
    service = _build_service(collection)
    customer = service.create_customer(payload)
    return CustomerResponseDTO.model_validate(customer)


@router.get("", response_model=List[CustomerResponseDTO], status_code=status.HTTP_200_OK)
def get_customers(collection: CollectionDep):
    service = _build_service(collection)
    customers = service.get_all_customers()
    return [CustomerResponseDTO.model_validate(item) for item in customers]


@router.get("/{customer_id}", response_model=CustomerResponseDTO, status_code=status.HTTP_200_OK)
def get_customer(customer_id: int, collection: CollectionDep):
    service = _build_service(collection)
    customer = service.get_customer(customer_id)
    return CustomerResponseDTO.model_validate(customer)


@router.put("/{customer_id}", response_model=CustomerResponseDTO, status_code=status.HTTP_200_OK)
def update_customer(customer_id: int, payload: CustomerUpdateDTO, collection: CollectionDep):
    service = _build_service(collection)
    customer = service.update_customer(customer_id, payload)
    return CustomerResponseDTO.model_validate(customer)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, collection: CollectionDep):
    service = _build_service(collection)
    service.delete_customer(customer_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
