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
