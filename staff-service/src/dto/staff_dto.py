from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class StaffCreateRequest(BaseModel):
    name: str = Field(..., min_length=2)
    email: Optional[str] = None
    phone: str = Field(..., min_length=7)
    specialty: str
    experience_years: int = Field(..., ge=0)
    availability: Optional[Literal["available", "unavailable"]] = "available"

    model_config = {"populate_by_name": True}


class StaffUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    email: Optional[str] = None
    phone: Optional[str] = Field(None, min_length=7)
    specialty: Optional[str] = None
    experience_years: Optional[int] = Field(None, ge=0)
    workload: Optional[int] = None
    availability: Optional[Literal["available", "unavailable"]] = None

    model_config = {"populate_by_name": True}


class StaffResponse(BaseModel):
    id: str
    name: str
    email: Optional[str] = None
    phone: str
    specialty: str
    experience_years: int
    workload: int
    availability: str
    created_at: datetime

    model_config = {"populate_by_name": True}
