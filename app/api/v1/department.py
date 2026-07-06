from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.exceptions import DepartmentNotFoundError
from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.api_response import ApiResponse
from app.schemas.department import DepartmentCreate, DepartmentResponse, DepartmentListResponse
from app.services.department_service import DepartmentService
from app.utils.pagination import get_paginated_data

router = APIRouter(prefix="/api/v1/departments", tags=["departments"])


@router.post("",response_model=ApiResponse[DepartmentResponse],status_code=status.HTTP_201_CREATED,)
def create_department(
    payload: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = DepartmentService(db)
    try:
        department = service.create_department(
            name=payload.name,
            description=payload.description,
            created_by=current_user.id,
        )
    except ValueError as e:
        if "already exists" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e),
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return ApiResponse(
        success=True,
        message="Department created successfully",
        data=DepartmentResponse.model_validate(department),
    )


@router.get("",response_model=ApiResponse[DepartmentListResponse],status_code=status.HTTP_200_OK,)
def get_all_departments(
    request: Request,
    skip: int = 0,
    limit: int = 12,
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = DepartmentService(db)
    departments, total = service.get_all_departments(
        skip=skip, limit=limit, search=search
    )
    paginated_data = get_paginated_data(
        items=departments,
        total=total,
        skip=skip,
        limit=limit,
        base_path=request.url.path,
        extra_params={"search": search},
    )
    return ApiResponse(
        success=True,
        message="Departments retrieved successfully",
        data=DepartmentListResponse(**paginated_data),
    )


@router.get("/{department_id}", response_model=ApiResponse[DepartmentResponse], status_code=status.HTTP_200_OK)
def get_department_by_id(
    department_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = DepartmentService(db)
    try:
        department = service.get_department_by_id(department_id)
    except DepartmentNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    return ApiResponse(
        success=True,
        message="Department retrieved successfully",
        data=DepartmentResponse.model_validate(department),
    )

