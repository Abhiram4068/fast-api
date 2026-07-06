from typing import Any, Generic, TypeVar
from pydantic import BaseModel
from urllib.parse import urlencode

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    skip: int
    limit: int
    next: str | None = None
    previous: str | None = None


def get_paginated_data(
    items: list[Any],
    total: int,
    skip: int,
    limit: int,
    base_path: str,
    extra_params: dict[str, Any] | None = None
) -> dict[str, Any]:
    """
    Constructs pagination data including next and previous page path-based URLs.
    Filters out pagination query parameters from extra_params to prevent duplicates.
    """
    # Filter out None values and skip/limit from extra_params
    cleaned_params = {}
    if extra_params:
        for k, v in extra_params.items():
            if v is not None and k not in ("skip", "limit"):
                cleaned_params[k] = v

    next_link = None
    if skip + limit < total:
        next_params = {"skip": skip + limit, "limit": limit, **cleaned_params}
        next_link = f"{base_path}?{urlencode(next_params)}"

    prev_link = None
    if skip > 0:
        prev_skip = max(0, skip - limit)
        prev_params = {"skip": prev_skip, "limit": limit, **cleaned_params}
        prev_link = f"{base_path}?{urlencode(prev_params)}"

    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit,
        "next": next_link,
        "previous": prev_link
    }
