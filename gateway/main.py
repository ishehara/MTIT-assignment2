from pathlib import Path
import sys
from typing import Any, List, Optional

import httpx
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field

from config import settings
from errors import ServiceError, general_exception_handler, service_error_handler
from middleware import LoggingMiddleware

# Add project root to path to import the shared db package.
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from db.mongo import check_mongo_connection  # noqa: E402

app = FastAPI(
    title="API Gateway",
    version="2.0.0",
    description="Gateway with inventory routes and shared MongoDB status check",
)

app.add_middleware(LoggingMiddleware)
app.add_exception_handler(ServiceError, service_error_handler)
app.add_exception_handler(Exception, general_exception_handler)

INVENTORY_SERVICE_URL = settings.INVENTORY_SERVICE_URL
CUSTOMER_SERVICE_URL = settings.CUSTOMER_SERVICE_URL


class InventoryCreate(BaseModel):
    name: str = Field(..., min_length=2)
    description: str = Field(..., min_length=2)
    quantity: int = Field(..., ge=0)
    price: float = Field(..., ge=0)


class InventoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    description: Optional[str] = Field(None, min_length=2)
    quantity: Optional[int] = Field(None, ge=0)
    price: Optional[float] = Field(None, ge=0)


class CustomerCreate(BaseModel):
    customer_id: int = Field(..., ge=1)
    name: str = Field(..., min_length=2)
    phone: str = Field(..., min_length=7)
    email: EmailStr
    address: str = Field(..., min_length=5)
    device_type: str = Field(..., min_length=2)
    device_issue: str = Field(..., min_length=2)
    device_status: str = Field(..., min_length=2)
    repair_history: List[str] = Field(default_factory=list)


class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    phone: Optional[str] = Field(None, min_length=7)
    email: Optional[EmailStr] = None
    address: Optional[str] = Field(None, min_length=5)
    device_type: Optional[str] = Field(None, min_length=2)
    device_issue: Optional[str] = Field(None, min_length=2)
    device_status: Optional[str] = Field(None, min_length=2)
    repair_history: Optional[List[str]] = None


async def forward_service_request(
    service_name: str,
    base_url: str,
    path: str,
    method: str,
    **kwargs,
) -> Any:
    url = f"{base_url}{path}"

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            if method == "GET":
                response = await client.get(url, **kwargs)
            elif method == "POST":
                response = await client.post(url, **kwargs)
            elif method == "PUT":
                response = await client.put(url, **kwargs)
            elif method == "DELETE":
                response = await client.delete(url, **kwargs)
            else:
                raise ServiceError(
                    message=f"HTTP method '{method}' not allowed",
                    status_code=405,
                    service_name=service_name,
                )

            if response.status_code >= 500:
                raise ServiceError(
                    message=f"{service_name} service error: {response.text}",
                    status_code=response.status_code,
                    service_name=service_name,
                )

            return JSONResponse(
                content=response.json() if response.text else None,
                status_code=response.status_code,
            )
        except httpx.TimeoutException as exc:
            raise ServiceError(
                message=f"{service_name} service timeout - request took too long",
                status_code=504,
                service_name=service_name,
            ) from exc
        except httpx.ConnectError as exc:
            raise ServiceError(
                message=f"{service_name} service unavailable - cannot connect to service",
                status_code=503,
                service_name=service_name,
            ) from exc
        except httpx.RequestError as exc:
            raise ServiceError(
                message=f"{service_name} service error: {str(exc)}",
                status_code=503,
                service_name=service_name,
            ) from exc


async def forward_inventory_request(path: str, method: str, **kwargs) -> Any:
    return await forward_service_request("inventory", INVENTORY_SERVICE_URL, path, method, **kwargs)


async def forward_customer_request(path: str, method: str, **kwargs) -> Any:
    return await forward_service_request("customer", CUSTOMER_SERVICE_URL, path, method, **kwargs)


@app.get("/")
def read_root():
    return {
        "message": "API Gateway is running",
        "version": "2.0.0",
        "available_services": ["inventory", "customer"],
        "database": {
            "provider": "MongoDB",
            "status": "UP" if check_mongo_connection() else "DOWN",
        },
    }


@app.get("/gateway/inventory", tags=["Inventory"])
async def get_inventory_items():
    return await forward_inventory_request("/api/inventory", "GET")


@app.get("/gateway/inventory/{item_id}", tags=["Inventory"])
async def get_inventory_item(item_id: str):
    return await forward_inventory_request(f"/api/inventory/{item_id}", "GET")


@app.post("/gateway/inventory", tags=["Inventory"])
async def create_inventory_item(item: InventoryCreate):
    return await forward_inventory_request("/api/inventory", "POST", json=item.model_dump())


@app.put("/gateway/inventory/{item_id}", tags=["Inventory"])
async def update_inventory_item(item_id: str, item: InventoryUpdate):
    return await forward_inventory_request(
        f"/api/inventory/{item_id}",
        "PUT",
        json=item.model_dump(exclude_unset=True),
    )


@app.delete("/gateway/inventory/{item_id}", tags=["Inventory"])
async def delete_inventory_item(item_id: str):
    return await forward_inventory_request(f"/api/inventory/{item_id}", "DELETE")


@app.get("/gateway/customers", tags=["Customers"])
async def get_customers():
    return await forward_customer_request("/api/customers", "GET")


@app.get("/gateway/customers/{customer_id}", tags=["Customers"])
async def get_customer(customer_id: int):
    return await forward_customer_request(f"/api/customers/{customer_id}", "GET")


@app.post("/gateway/customers", tags=["Customers"])
async def create_customer(payload: CustomerCreate):
    return await forward_customer_request("/api/customers", "POST", json=payload.model_dump())


@app.put("/gateway/customers/{customer_id}", tags=["Customers"])
async def update_customer(customer_id: int, payload: CustomerUpdate):
    return await forward_customer_request(
        f"/api/customers/{customer_id}",
        "PUT",
        json=payload.model_dump(exclude_unset=True),
    )


@app.delete("/gateway/customers/{customer_id}", tags=["Customers"])
async def delete_customer(customer_id: int):
    return await forward_customer_request(f"/api/customers/{customer_id}", "DELETE")
 