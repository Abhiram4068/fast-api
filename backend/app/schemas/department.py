import re

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.utils.pagination import PaginatedResponse

class DepartmentBase(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
        examples=["Information Technology"],
    )

    description: str | None = Field(
        default=None,
        max_length=255,
        examples=["Handles all IT operations."],
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Department name cannot be empty.")
        value = re.sub(r"\s+", " ", value)

        if not re.fullmatch(r"[A-Za-z0-9&()/\- ]+", value):
            raise ValueError(
                "Department name contains invalid characters."
            )

        if re.match(r"^[&()/\-]", value) or re.search(r"[&()/\-]$", value):
            raise ValueError(
                "Department name cannot start or end with a special character."
            )

        return value


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=255,
    )

    is_active: bool | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()

        if not value:
            raise ValueError("Department name cannot be empty.")
        value = re.sub(r"\s+", " ", value)

        if not re.fullmatch(r"[A-Za-z0-9&()/\- ]+", value):
            raise ValueError(
                "Department name contains invalid characters."
            )

        if re.match(r"^[&()/\-]", value) or re.search(r"[&()/\-]$", value):
            raise ValueError(
                "Department name cannot start or end with a special character."
            )
            
        return value



class DepartmentResponse(DepartmentBase):
    id: UUID
    is_active: bool
    created_by: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)



class DepartmentListResponse(PaginatedResponse[DepartmentResponse]):
    pass