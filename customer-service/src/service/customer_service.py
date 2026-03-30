from typing import Any, Dict, List

from src.dto.customer_dto import CustomerCreateDTO, CustomerUpdateDTO
from src.errors.exceptions import CustomerConflictException, CustomerNotFoundException
from src.repository.customer_repository import CustomerRepository


class CustomerService:
    def __init__(self, collection):
        self.repository = CustomerRepository(collection)

    def create_customer(self, payload: CustomerCreateDTO) -> Dict[str, Any]:
        if self.repository.exists_by_customer_id(payload.customer_id):
            raise CustomerConflictException(
                f"Customer with id {payload.customer_id} already exists",
            )
        return self.repository.create(payload.model_dump())

    def get_all_customers(self) -> List[Dict[str, Any]]:
        return self.repository.find_all()

    def get_customer(self, customer_id: int) -> Dict[str, Any]:
        customer = self.repository.find_by_customer_id(customer_id)
        if not customer:
            raise CustomerNotFoundException(
                f"Customer with id {customer_id} not found",
            )
        return customer

    def update_customer(self, customer_id: int, payload: CustomerUpdateDTO) -> Dict[str, Any]:
        if payload.model_fields_set == set():
            return self.get_customer(customer_id)
        update_data = payload.model_dump(exclude_unset=True)
        updated = self.repository.update_by_customer_id(customer_id, update_data)
        if not updated:
            raise CustomerNotFoundException(
                f"Customer with id {customer_id} not found",
            )
        return updated

    def delete_customer(self, customer_id: int) -> None:
        if not self.repository.delete_by_customer_id(customer_id):
            raise CustomerNotFoundException(
                f"Customer with id {customer_id} not found",
            )
