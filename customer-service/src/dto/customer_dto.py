from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CustomerCreateDTO(BaseModel):
    customer_id: int = Field(..., ge=1)
    name: str = Field(..., min_length=2, max_length=120)
    phone: str = Field(..., min_length=7, max_length=20)
    email: EmailStr
    address: str = Field(..., min_length=5, max_length=300)
    customer_nic: str = Field(..., min_length=5, max_length=20)


class CustomerUpdateDTO(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=120)
    phone: Optional[str] = Field(None, min_length=7, max_length=20)
    email: Optional[EmailStr] = None
    address: Optional[str] = Field(None, min_length=5, max_length=300)
    customer_nic: Optional[str] = Field(None, min_length=5, max_length=20)


class CustomerResponseDTO(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    customer_id: int
    name: str
    phone: str
    email: EmailStr
    address: str
    customer_nic: str
    createdAt: datetime
    updatedAt: datetime
