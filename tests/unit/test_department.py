import pytest
from uuid import uuid4
from app.repositories.department_repository import DepartmentRepository
from app.repositories.user_repository import UserRepository
from app.services.department_service import DepartmentService
from app.core.exceptions import DepartmentNotFoundError

@pytest.fixture
def test_user(db_session):
    user_repo = UserRepository(db_session)
    return user_repo.create_user(
        username="dept_creator",
        email="creator@example.com",
        hashed_password="hashed_password_123"
    )

# ------------------------------------------------------------------ #
# Repository Tests
# ------------------------------------------------------------------ #

def test_repo_create_department(db_session, test_user):
    repo = DepartmentRepository(db_session)
    dept = repo.create(
        name="Engineering",
        description="Software development department",
        created_by=test_user.id
    )
    assert dept.id is not None
    assert dept.name == "Engineering"
    assert dept.description == "Software development department"
    assert dept.created_by == test_user.id
    assert dept.is_active is True


def test_repo_get_by_name(db_session, test_user):
    repo = DepartmentRepository(db_session)
    repo.create(name="HR", description=None, created_by=test_user.id)
    
    found = repo.get_by_name("hr")
    assert found is not None
    assert found.name == "HR"
    
    not_found = repo.get_by_name("nonexistent")
    assert not_found is None


def test_repo_get_by_id(db_session, test_user):
    repo = DepartmentRepository(db_session)
    dept = repo.create(name="Finance", description=None, created_by=test_user.id)
    
    found = repo.get_by_id(dept.id)
    assert found is not None
    assert found.id == dept.id
    
    assert repo.get_by_id(uuid4()) is None


def test_repo_get_all_and_count(db_session, test_user):
    repo = DepartmentRepository(db_session)
    repo.create(name="Sales", description=None, created_by=test_user.id)
    repo.create(name="Marketing", description=None, created_by=test_user.id)
    
    results = repo.get_all(skip=0, limit=10)
    assert len(results) == 2
    # Alphabetical order: Marketing, Sales
    assert results[0].name == "Marketing"
    assert results[1].name == "Sales"
    
    assert repo.count() == 2
    
    # Test search filter
    search_results = repo.get_all(skip=0, limit=10, search="sal")
    assert len(search_results) == 1
    assert search_results[0].name == "Sales"
    assert repo.count(search="sal") == 1


# ------------------------------------------------------------------ #
# Service Tests
# ------------------------------------------------------------------ #

def test_service_create_department_success(db_session, test_user):
    service = DepartmentService(db_session)
    dept = service.create_department(
        name="QA Department",
        description="Quality assurance",
        created_by=test_user.id
    )
    assert dept.name == "QA Department"


def test_service_create_department_duplicate_raises(db_session, test_user):
    service = DepartmentService(db_session)
    service.create_department(name="Legal", description=None, created_by=test_user.id)
    
    with pytest.raises(ValueError, match="Department already exists"):
        service.create_department(name="legal", description="dup", created_by=test_user.id)


def test_service_get_all_departments(db_session, test_user):
    service = DepartmentService(db_session)
    service.create_department(name="IT", description=None, created_by=test_user.id)
    
    depts, total = service.get_all_departments(skip=0, limit=10)
    assert total == 1
    assert len(depts) == 1
    assert depts[0].name == "IT"


def test_service_get_department_by_id_success(db_session, test_user):
    service = DepartmentService(db_session)
    dept = service.create_department(name="Operations", description=None, created_by=test_user.id)
    
    found = service.get_department_by_id(dept.id)
    assert found.id == dept.id


def test_service_get_department_by_id_raises_not_found(db_session):
    service = DepartmentService(db_session)
    with pytest.raises(DepartmentNotFoundError, match="Department not found"):
        service.get_department_by_id(uuid4())
