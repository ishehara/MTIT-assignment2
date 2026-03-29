from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RepairStatus(str, Enum):
    NOT_STARTED = "not_started"
    REPAIRING = "repairing"
    FINISHED = "finished"
    HANDED_OVER = "handed_over"


class RepairJobCreateDTO(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=120)
    customer_phone: str = Field(..., min_length=7, max_length=20)
    customer_email: Optional[str] = Field(None, max_length=254)
    device_type: str = Field(..., min_length=2, max_length=60)
    device_brand: str = Field(..., min_length=1, max_length=60)
    device_model: str = Field(..., min_length=1, max_length=60)
    issue_description: str = Field(..., min_length=5, max_length=1000)


class RepairJobUpdateStatusDTO(BaseModel):
    status: Optional[RepairStatus] = None
    technician_notes: Optional[str] = Field(None, max_length=1000)


class RepairJobUpdateDTO(BaseModel):
    customer_name: Optional[str] = Field(None, min_length=2, max_length=120)
    customer_phone: Optional[str] = Field(None, min_length=7, max_length=20)
    customer_email: Optional[str] = Field(None, max_length=254)
    device_type: Optional[str] = Field(None, min_length=2, max_length=60)
    device_brand: Optional[str] = Field(None, min_length=1, max_length=60)
    device_model: Optional[str] = Field(None, min_length=1, max_length=60)
    issue_description: Optional[str] = Field(None, min_length=5, max_length=1000)


class RepairJobResponseDTO(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    customer_name: str
    customer_phone: str
    customer_email: Optional[str]
    device_type: str
    device_brand: str
    device_model: str
    issue_description: str
    status: RepairStatus
    technician_notes: Optional[str]
    created_at: datetime
    updated_at: datetime
