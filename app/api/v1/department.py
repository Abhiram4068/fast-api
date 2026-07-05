from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.api_response import ApiResponse
from app.schemas.department import DepartmentCreate, DepartmentResponse
from app.services.department_service import DepartmentService

router = APIRouter(prefix="/api/v1/departments", tags=["departments"])


@router.post(
    "",
    response_model=ApiResponse[DepartmentResponse],
    status_code=status.HTTP_201_CREATED,
)
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

