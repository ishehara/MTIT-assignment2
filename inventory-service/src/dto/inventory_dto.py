from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class InventoryCreateDTO(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=120,
        description="Item name (2-120 characters, must contain at least one letter)"
    )
    description: str = Field(
        ...,
        min_length=2,
        max_length=500,
        description="Item description (2-500 characters, non-empty)"
    )
    quantity: int = Field(
        ...,
        ge=0,
        le=1000000,
        description="Item quantity (0-1,000,000)"
    )
    price: float = Field(
        ...,
        ge=0,
        le=9999999.99,
        description="Item price (0-9,999,999.99, rounded to 2 decimals)"
    )
    supplier: str = Field(
        ...,
        min_length=2,
        max_length=120,
        description="Supplier name (2-120 characters, must contain at least one letter)"
    )
    condition: str = Field(
        ...,
        min_length=2,
        max_length=120,
        description="Item condition (one of: New, Refurbished, Used, Damaged)"
    )
    warranty_period: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Warranty period (1-50 characters, cannot be empty)"
    )

    @field_validator('name', mode='after')
    @classmethod
    def validate_name(cls, v):
        """Validate name field: non-empty, must contain alphabetic characters."""
        if not v or not v.strip():
            raise ValueError('Name is required and cannot contain only whitespace')
        if not any(c.isalpha() for c in v):
            raise ValueError('Name must contain at least one alphabetic character (a-z, A-Z)')
        return v.strip()

    @field_validator('description', mode='after')
    @classmethod
    def validate_description(cls, v):
        """Validate description field: non-empty, meaningful content."""
        if not v or not v.strip():
            raise ValueError('Description is required and cannot contain only whitespace')
        if len(v.strip()) < 2:
            raise ValueError('Description must be at least 2 characters long (excluding whitespace)')
        return v.strip()

    @field_validator('supplier', mode='after')
    @classmethod
    def validate_supplier(cls, v):
        """Validate supplier field: non-empty, must contain alphabetic characters."""
        if not v or not v.strip():
            raise ValueError('Supplier name is required and cannot contain only whitespace')
        if not any(c.isalpha() for c in v):
            raise ValueError('Supplier name must contain at least one alphabetic character (a-z, A-Z)')
        return v.strip()

    @field_validator('condition', mode='after')
    @classmethod
    def validate_condition(cls, v):
        """Validate condition field: must be one of predefined options."""
        valid_conditions = ['New', 'Refurbished', 'Used', 'Damaged']
        if v not in valid_conditions:
            raise ValueError(
                f"Invalid condition '{v}'. Must be one of: {', '.join(valid_conditions)}"
            )
        return v

    @field_validator('warranty_period', mode='after')
    @classmethod
    def validate_warranty_period(cls, v):
        """Validate warranty_period field: non-empty and meaningful."""
        if not v or not v.strip():
            raise ValueError('Warranty period is required and cannot be empty or contain only whitespace')
        if len(v.strip()) < 1:
            raise ValueError('Warranty period must be at least 1 character long')
        return v.strip()

    @field_validator('price', mode='after')
    @classmethod
    def validate_price(cls, v):
        """Validate price field: non-negative, within range, rounded to 2 decimals."""
        if v < 0:
            raise ValueError('Price cannot be negative. Please provide a price >= 0')
        if v > 9999999.99:
            raise ValueError('Price cannot exceed 9,999,999.99')
        # Round to 2 decimal places
        return round(v, 2)

    @field_validator('quantity', mode='after')
    @classmethod
    def validate_quantity(cls, v):
        """Validate quantity field: non-negative integer within range."""
        if v < 0:
            raise ValueError('Quantity cannot be negative. Please provide a quantity >= 0')
        if v > 1000000:
            raise ValueError('Quantity cannot exceed 1,000,000 units')
        return v


class InventoryUpdateDTO(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=120,
        description="Item name (2-120 characters, must contain at least one letter)"
    )
    description: Optional[str] = Field(
        None,
        min_length=2,
        max_length=500,
        description="Item description (2-500 characters, non-empty)"
    )
    quantity: Optional[int] = Field(
        None,
        ge=0,
        le=1000000,
        description="Item quantity (0-1,000,000)"
    )
    price: Optional[float] = Field(
        None,
        ge=0,
        le=9999999.99,
        description="Item price (0-9,999,999.99, rounded to 2 decimals)"
    )
    supplier: Optional[str] = Field(
        None,
        min_length=2,
        max_length=120,
        description="Supplier name (2-120 characters, must contain at least one letter)"
    )
    condition: Optional[str] = Field(
        None,
        min_length=2,
        max_length=120,
        description="Item condition (one of: New, Refurbished, Used, Damaged)"
    )
    warranty_period: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50,
        description="Warranty period (1-50 characters, cannot be empty)"
    )

    @field_validator('name', mode='after')
    @classmethod
    def validate_name(cls, v):
        """Validate name field: non-empty, must contain alphabetic characters."""
        if v is not None:
            if not v or not v.strip():
                raise ValueError('Name is required and cannot contain only whitespace')
            if not any(c.isalpha() for c in v):
                raise ValueError('Name must contain at least one alphabetic character (a-z, A-Z)')
            return v.strip()
        return v

    @field_validator('description', mode='after')
    @classmethod
    def validate_description(cls, v):
        """Validate description field: non-empty, meaningful content."""
        if v is not None:
            if not v or not v.strip():
                raise ValueError('Description is required and cannot contain only whitespace')
            if len(v.strip()) < 2:
                raise ValueError('Description must be at least 2 characters long (excluding whitespace)')
            return v.strip()
        return v

    @field_validator('supplier', mode='after')
    @classmethod
    def validate_supplier(cls, v):
        """Validate supplier field: non-empty, must contain alphabetic characters."""
        if v is not None:
            if not v or not v.strip():
                raise ValueError('Supplier name is required and cannot contain only whitespace')
            if not any(c.isalpha() for c in v):
                raise ValueError('Supplier name must contain at least one alphabetic character (a-z, A-Z)')
            return v.strip()
        return v

    @field_validator('condition', mode='after')
    @classmethod
    def validate_condition(cls, v):
        """Validate condition field: must be one of predefined options."""
        if v is not None:
            valid_conditions = ['New', 'Refurbished', 'Used', 'Damaged']
            if v not in valid_conditions:
                raise ValueError(
                    f"Invalid condition '{v}'. Must be one of: {', '.join(valid_conditions)}"
                )
            return v
        return v

    @field_validator('warranty_period', mode='after')
    @classmethod
    def validate_warranty_period(cls, v):
        """Validate warranty_period field: non-empty and meaningful."""
        if v is not None:
            if not v or not v.strip():
                raise ValueError('Warranty period is required and cannot be empty or contain only whitespace')
            if len(v.strip()) < 1:
                raise ValueError('Warranty period must be at least 1 character long')
            return v.strip()
        return v

    @field_validator('price', mode='after')
    @classmethod
    def validate_price(cls, v):
        """Validate price field: non-negative, within range, rounded to 2 decimals."""
        if v is not None:
            if v < 0:
                raise ValueError('Price cannot be negative. Please provide a price >= 0')
            if v > 9999999.99:
                raise ValueError('Price cannot exceed 9,999,999.99')
            return round(v, 2)
        return v

    @field_validator('quantity', mode='after')
    @classmethod
    def validate_quantity(cls, v):
        """Validate quantity field: non-negative integer within range."""
        if v is not None:
            if v < 0:
                raise ValueError('Quantity cannot be negative. Please provide a quantity >= 0')
            if v > 1000000:
                raise ValueError('Quantity cannot exceed 1,000,000 units')
            return v
        return v


class InventoryResponseDTO(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str
    description: str
    quantity: int
    price: float
    supplier: str
    condition: str
    warranty_period: str
    createdAt: datetime


class MessageResponseDTO(BaseModel):
    message: str
    status: str
