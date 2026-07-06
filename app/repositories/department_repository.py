from uuid import UUID
from sqlalchemy.orm import Session
from app.models.departments import Department
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

    def get_all(self,skip: int = 0,limit: int = 100,search: str | None = None,) -> list[Department]:

        query = self.db.query(Department)

        if search:
            query = query.filter(func.lower(Department.name).contains(search.lower()))

        return (
            query
            .order_by(Department.name.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count(self, search: str | None = None) -> int:
        query = self.db.query(func.count(Department.id))
        if search:
            query = query.filter(func.lower(Department.name).contains(search.lower()))
        return query.scalar() or 0

    def get_by_name(self, name: str) -> Department | None:       
        return (
            self.db.query(Department)
            .filter(func.lower(Department.name) == name.lower())
            .first()
        )

    def get_by_id(self, department_id: UUID) -> Department | None:
        return self.db.query(Department).filter(Department.id == department_id).first()

