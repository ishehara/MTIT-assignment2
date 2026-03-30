from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class InventoryCreateDTO(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    description: str = Field(..., min_length=2, max_length=500)
    quantity: int = Field(..., ge=0)
    price: float = Field(..., ge=0)


class InventoryUpdateDTO(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=120)
    description: Optional[str] = Field(None, min_length=2, max_length=500)
    quantity: Optional[int] = Field(None, ge=0)
    price: Optional[float] = Field(None, ge=0)


class InventoryResponseDTO(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str
    description: str
    quantity: int
    price: float
    createdAt: datetime


class MessageResponseDTO(BaseModel):
    message: str
    status: str
