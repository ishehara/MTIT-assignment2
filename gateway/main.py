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
REPAIR_SERVICE_URL = settings.REPAIR_SERVICE_URL
STAFF_SERVICE_URL = settings.STAFF_SERVICE_URL


# ---------------------------------------------------------------------------
# Repair service helpers
# ---------------------------------------------------------------------------

async def forward_repair_request(path: str, method: str, **kwargs) -> Any:
    url = f"{REPAIR_SERVICE_URL}{path}"

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            if method == "GET":
                response = await client.get(url, **kwargs)
            elif method == "POST":
                response = await client.post(url, **kwargs)
            elif method == "PATCH":
                response = await client.patch(url, **kwargs)
            elif method == "PUT":
                response = await client.put(url, **kwargs)
            elif method == "DELETE":
                response = await client.delete(url, **kwargs)
            else:
                raise ServiceError(
                    message=f"HTTP method '{method}' not allowed",
                    status_code=405,
                    service_name="repair",
                )

            if response.status_code >= 500:
                raise ServiceError(
                    message=f"repair service error: {response.text}",
                    status_code=response.status_code,
                    service_name="repair",
                )

            return JSONResponse(
                content=response.json() if response.text else None,
                status_code=response.status_code,
            )
        except httpx.TimeoutException as exc:
            raise ServiceError(
                message="repair service timeout - request took too long",
                status_code=504,
                service_name="repair",
            ) from exc
        except httpx.ConnectError as exc:
            raise ServiceError(
                message="repair service unavailable - cannot connect to service",
                status_code=503,
                service_name="repair",
            ) from exc
        except httpx.RequestError as exc:
            raise ServiceError(
                message=f"repair service error: {str(exc)}",
                status_code=503,
                service_name="repair",
            ) from exc


# ---------------------------------------------------------------------------
# Repair request/response models
# ---------------------------------------------------------------------------

class RepairJobCreate(BaseModel):
    customer_name: str = Field(..., min_length=2)
    customer_phone: str = Field(..., min_length=7)
    customer_email: Optional[str] = None
    device_type: str = Field(..., min_length=2)
    device_brand: str = Field(..., min_length=1)
    device_model: str = Field(..., min_length=1)
    issue_description: str = Field(..., min_length=5)


class RepairStatusUpdate(BaseModel):
    status: str
    technician_notes: Optional[str] = None


class RepairJobUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_email: Optional[str] = None
    device_type: Optional[str] = None
    device_brand: Optional[str] = None
    device_model: Optional[str] = None
    issue_description: Optional[str] = None


# ---------------------------------------------------------------------------
# Inventory models
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Staff models
# ---------------------------------------------------------------------------

class StaffCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: Optional[str] = None
    phone: str = Field(..., min_length=7)
    specialty: str
    status: Optional[str] = "active"


class StaffUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    email: Optional[str] = None
    phone: Optional[str] = Field(None, min_length=7)
    specialty: Optional[str] = None
    workload: Optional[int] = None
    status: Optional[str] = None


async def forward_inventory_request(path: str, method: str, **kwargs) -> Any:
    url = f"{INVENTORY_SERVICE_URL}{path}"
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


# ---------------------------------------------------------------------------
# Staff service helpers
# ---------------------------------------------------------------------------

async def forward_staff_request(path: str, method: str, **kwargs) -> Any:
    url = f"{STAFF_SERVICE_URL}{path}"

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
                    service_name="staff",
                )

            if response.status_code >= 500:
                raise ServiceError(
                    message=f"staff service error: {response.text}",
                    status_code=response.status_code,
                    service_name="staff",
                )

            return JSONResponse(
                content=response.json() if response.text else None,
                status_code=response.status_code,
            )
        except httpx.TimeoutException as exc:
            raise ServiceError(
                message="staff service timeout - request took too long",
                status_code=504,
                service_name="staff",
            ) from exc
        except httpx.ConnectError as exc:
            raise ServiceError(
                message="staff service unavailable - cannot connect to service",
                status_code=503,
                service_name="staff",
            ) from exc
        except httpx.RequestError as exc:
            raise ServiceError(
                message=f"staff service error: {str(exc)}",
                status_code=503,
                service_name="staff",
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
        "available_services": ["inventory", "repair", "staff", "customer"],
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
# ---------------------------------------------------------------------------
# Repair service routes
# ---------------------------------------------------------------------------

@app.post("/gateway/repairs", tags=["Repair"])
async def register_device(job: RepairJobCreate):
    return await forward_repair_request("/api/repairs", "POST", json=job.model_dump())


@app.get("/gateway/repairs", tags=["Repair"])
async def get_all_repair_jobs():
    return await forward_repair_request("/api/repairs", "GET")


@app.get("/gateway/repairs/status/{status}", tags=["Repair"])
async def get_repair_jobs_by_status(status: str):
    return await forward_repair_request(f"/api/repairs/status/{status}", "GET")


@app.get("/gateway/repairs/{job_id}", tags=["Repair"])
async def get_repair_job(job_id: str):
    return await forward_repair_request(f"/api/repairs/{job_id}", "GET")


@app.put("/gateway/repairs/{job_id}", tags=["Repair"])
async def update_repair_job(job_id: str, payload: RepairJobUpdate):
    return await forward_repair_request(
        f"/api/repairs/{job_id}",
        "PUT",
        json=payload.model_dump(exclude_unset=True),
    )


@app.delete("/gateway/customers/{customer_id}", tags=["Customers"])
async def delete_customer(customer_id: int):
    return await forward_customer_request(f"/api/customers/{customer_id}", "DELETE")
 
@app.patch("/gateway/repairs/{job_id}/status", tags=["Repair"])
async def update_repair_status(job_id: str, payload: RepairStatusUpdate):
    return await forward_repair_request(
        f"/api/repairs/{job_id}/status",
        "PATCH",
        json=payload.model_dump(exclude_unset=True),
    )


@app.delete("/gateway/repairs/{job_id}", tags=["Repair"])
async def delete_repair_job(job_id: str):
    return await forward_repair_request(f"/api/repairs/{job_id}", "DELETE")


# ---------------------------------------------------------------------------
# Staff service routes
# ---------------------------------------------------------------------------

@app.post("/gateway/staff", tags=["Staff"])
async def create_staff(staff: StaffCreate):
    return await forward_staff_request("/api/staff", "POST", json=staff.model_dump())


@app.get("/gateway/staff", tags=["Staff"])
async def get_all_staff():
    return await forward_staff_request("/api/staff", "GET")


@app.get("/gateway/staff/{staff_id}", tags=["Staff"])
async def get_staff(staff_id: str):
    return await forward_staff_request(f"/api/staff/{staff_id}", "GET")


@app.put("/gateway/staff/{staff_id}", tags=["Staff"])
async def update_staff(staff_id: str, staff: StaffUpdate):
    return await forward_staff_request(
        f"/api/staff/{staff_id}",
        "PUT",
        json=staff.model_dump(exclude_unset=True),
    )


@app.delete("/gateway/staff/{staff_id}", tags=["Staff"])
async def delete_staff(staff_id: str):
    return await forward_staff_request(f"/api/staff/{staff_id}", "DELETE")
