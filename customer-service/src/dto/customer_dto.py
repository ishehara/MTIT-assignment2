from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CustomerCreateDTO(BaseModel):
    customer_id: int = Field(..., ge=1)
    name: str = Field(..., min_length=2, max_length=120)
    phone: str = Field(..., min_length=7, max_length=20)
    email: EmailStr
    address: str = Field(..., min_length=5, max_length=300)
    device_type: str = Field(..., min_length=2, max_length=80)
    device_issue: str = Field(..., min_length=2, max_length=500)
    device_status: str = Field(..., min_length=2, max_length=80)
    repair_history: List[str] = Field(default_factory=list)


class CustomerUpdateDTO(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=120)
    phone: Optional[str] = Field(None, min_length=7, max_length=20)
    email: Optional[EmailStr] = None
    address: Optional[str] = Field(None, min_length=5, max_length=300)
    device_type: Optional[str] = Field(None, min_length=2, max_length=80)
    device_issue: Optional[str] = Field(None, min_length=2, max_length=500)
    device_status: Optional[str] = Field(None, min_length=2, max_length=80)
    repair_history: Optional[List[str]] = None


class CustomerResponseDTO(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    customer_id: int
    name: str
    phone: str
    email: EmailStr
    address: str
    device_type: str
    device_issue: str
    device_status: str
    repair_history: List[str]
    createdAt: datetime
    updatedAt: datetime
