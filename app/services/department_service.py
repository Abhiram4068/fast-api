from uuid import UUID
from app.repositories.department_repository import DepartmentRepository
from app.models.departments import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate
from sqlalchemy.orm import Session

class DepartmentService:
    def __init__(self, db: Session):
        self.repository = DepartmentRepository(db)

    def create_department(self, name: str, description: str | None, created_by: UUID) -> Department:
        if self.repository.get_by_name(name):
            raise ValueError("Department already exists")
        return self.repository.create(name, description, created_by)



