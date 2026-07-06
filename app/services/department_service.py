from uuid import UUID
from app.repositories.department_repository import DepartmentRepository
from app.models.departments import Department
from sqlalchemy.orm import Session
from app.core.exceptions import DepartmentNotFoundError

class DepartmentService:
    def __init__(self, db: Session):
        self.repository = DepartmentRepository(db)

    def create_department(self, name: str, description: str | None, created_by: UUID) -> Department:
        if self.repository.get_by_name(name):
            raise ValueError("Department already exists")
        return self.repository.create(name, description, created_by)

    def get_all_departments(
        self,
        skip: int = 0,
        limit: int = 100,
        search: str | None = None,
    ) -> tuple[list[Department], int]:
        departments = self.repository.get_all(skip=skip, limit=limit, search=search)
        total = self.repository.count(search=search)
        return departments, total

    def get_department_by_id(self, department_id: UUID) -> Department:
        department = self.repository.get_by_id(department_id)
        if not department:
            raise DepartmentNotFoundError(f"Department not found")
        return department
