import pytest


@pytest.fixture
def auth_client(client):
    """Fixture to register and login a test user, returning the authenticated client."""
    # Register user
    register_payload = {
        "username": "deptmanager",
        "email": "manager@example.com",
        "password": "Password@123",
    }
    client.post("/api/v1/auth/register", json=register_payload)
    # Login to set cookies on client
    login_payload = {
        "email": "manager@example.com",
        "password": "Password@123",
    }
    login_response = client.post("/api/v1/auth/login", json=login_payload)
    assert login_response.status_code == 200
    assert "access_token" in login_response.cookies
    return client


def test_create_department_success(auth_client):
    payload = {
        "name": "Engineering Department",
        "description": "Handles software engineering tasks.",
    }
    response = auth_client.post("/api/v1/departments", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Department created successfully"
    assert data["data"]["name"] == "Engineering Department"
    assert data["data"]["description"] == "Handles software engineering tasks."
    assert "id" in data["data"]
    assert data["data"]["is_active"] is True
    assert "created_by" in data["data"]


def test_create_department_unauthenticated(client):
    payload = {
        "name": "Engineering Department",
        "description": "Handles software engineering tasks.",
    }
    response = client.post("/api/v1/departments", json=payload)
    
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]


def test_create_department_duplicate_name(auth_client):
    payload = {
        "name": "Human Resources",
        "description": "Handles HR tasks.",
    }
    # Create the first one
    response1 = auth_client.post("/api/v1/departments", json=payload)
    assert response1.status_code == 201

    # Try creating again with duplicate name (even with different description / spaces / cases)
    payload2 = {
        "name": " human resources  ",
        "description": "Duplicate HR.",
    }
    response2 = auth_client.post("/api/v1/departments", json=payload2)
    assert response2.status_code == 409
    assert "already exists" in response2.json()["detail"].lower()


def test_create_department_invalid_name(auth_client):
    # Department name too short
    response = auth_client.post("/api/v1/departments", json={"name": "A"})
    assert response.status_code == 422

    # Department name starts with special char
    response = auth_client.post("/api/v1/departments", json={"name": "&Engineering"})
    assert response.status_code == 422

    # Department name ends with special char
    response = auth_client.post("/api/v1/departments", json={"name": "Engineering-"})
    assert response.status_code == 422

    # Department name empty after strip
    response = auth_client.post("/api/v1/departments", json={"name": "   "})
    assert response.status_code == 422

    # Department name contains invalid characters
    response = auth_client.post("/api/v1/departments", json={"name": "IT Department #1"})
    assert response.status_code == 422


def test_get_all_departments_empty(auth_client, db_session):
    # Ensure database is clean or truncate department table if there's any data
    # (Since this is testing against the test DB setup, we can query or assume it starts fresh per test if session rollbacks work)
    from app.models.departments import Department
    db_session.query(Department).delete()
    db_session.commit()

    response = auth_client.get("/api/v1/departments")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["total"] == 0
    assert data["data"]["items"] == []
    assert data["data"]["skip"] == 0
    assert data["data"]["limit"] == 12
    assert data["data"]["next"] is None
    assert data["data"]["previous"] is None


def test_get_all_departments_success(auth_client):
    # Add a couple of departments
    auth_client.post("/api/v1/departments", json={"name": "Sales Dept", "description": "Sales team"})
    auth_client.post("/api/v1/departments", json={"name": "Marketing Dept", "description": "Marketing team"})

    response = auth_client.get("/api/v1/departments?skip=0&limit=1")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["total"] >= 2
    assert len(data["data"]["items"]) == 1
    assert data["data"]["skip"] == 0
    assert data["data"]["limit"] == 1
    assert data["data"]["next"] == "/api/v1/departments?skip=1&limit=1"
    assert data["data"]["previous"] is None


def test_get_all_departments_unauthenticated(client):
    response = client.get("/api/v1/departments")
    assert response.status_code == 401


def test_get_department_by_id_success(auth_client):
    # Create a department
    create_response = auth_client.post(
        "/api/v1/departments", 
        json={"name": "Support Dept", "description": "Support team"}
    )
    assert create_response.status_code == 201
    created_id = create_response.json()["data"]["id"]

    # Get by ID
    response = auth_client.get(f"/api/v1/departments/{created_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["id"] == created_id
    assert data["data"]["name"] == "Support Dept"
    assert data["data"]["description"] == "Support team"


def test_get_department_by_id_not_found(auth_client):
    import uuid
    random_id = str(uuid.uuid4())
    response = auth_client.get(f"/api/v1/departments/{random_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Department not found"


def test_get_department_by_id_unauthenticated(client):
    import uuid
    random_id = str(uuid.uuid4())
    response = client.get(f"/api/v1/departments/{random_id}")
    assert response.status_code == 401
