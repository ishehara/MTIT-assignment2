from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class StaffCreateRequest(BaseModel):
    name: str = Field(..., min_length=2)
    email: Optional[str] = None
    phone: str = Field(..., min_length=7)
    specialty: str
    status: Optional[Literal["active", "inactive"]] = "active"

    model_config = {"populate_by_name": True}


class StaffUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    email: Optional[str] = None
    phone: Optional[str] = Field(None, min_length=7)
    specialty: Optional[str] = None
    workload: Optional[int] = None
    status: Optional[Literal["active", "inactive"]] = None

    model_config = {"populate_by_name": True}


class StaffResponse(BaseModel):
    id: str
    name: str
    email: Optional[str] = None
    phone: str
    specialty: str
    workload: int
    status: str
    created_at: datetime

    model_config = {"populate_by_name": True}
