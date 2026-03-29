from pathlib import Path
import sys
from typing import Any, Optional

import httpx
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

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
REPAIR_SERVICE_URL = settings.REPAIR_SERVICE_URL


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


async def forward_inventory_request(path: str, method: str, **kwargs) -> Any:
    url = f"{INVENTORY_SERVICE_URL}{path}"

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
                    service_name="inventory",
                )

            if response.status_code >= 500:
                raise ServiceError(
                    message=f"inventory service error: {response.text}",
                    status_code=response.status_code,
                    service_name="inventory",
                )

            return JSONResponse(
                content=response.json() if response.text else None,
                status_code=response.status_code,
            )
        except httpx.TimeoutException as exc:
            raise ServiceError(
                message="inventory service timeout - request took too long",
                status_code=504,
                service_name="inventory",
            ) from exc
        except httpx.ConnectError as exc:
            raise ServiceError(
                message="inventory service unavailable - cannot connect to service",
                status_code=503,
                service_name="inventory",
            ) from exc
        except httpx.RequestError as exc:
            raise ServiceError(
                message=f"inventory service error: {str(exc)}",
                status_code=503,
                service_name="inventory",
            ) from exc


@app.get("/")
def read_root():
    return {
        "message": "API Gateway is running",
        "version": "2.0.0",
        "available_services": ["inventory", "repair"],
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
