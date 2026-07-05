from uuid import UUID
from sqlalchemy.orm import Session
from app.models.departments import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate
from sqlalchemy import func

class DepartmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, description: str | None, created_by: UUID) -> Department:
        db_department = Department(
            name=name,
            description=description,
            created_by=created_by
        )
        self.db.add(db_department)
        self.db.commit()
        self.db.refresh(db_department)
        return db_department


    def get_by_name(self, name: str) -> Department | None:
       
        return (
            self.db.query(Department)
            .filter(func.lower(Department.name) == name.lower())
            .first()
        )

    def get_by_id(self, department_id: UUID) -> Department | None:

        return self.db.query(Department).filter(Department.id == department_id).first()

