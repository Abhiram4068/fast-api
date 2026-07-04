def test_register_success_returns_201(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "johndoe",
            "email": "john@example.com",
            "password": "Password@123",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "johndoe"
    assert data["email"] == "john@example.com"
    assert data["message"] == "User registered successfully"
    assert "id" in data


def test_register_duplicate_email_returns_409(client):
    payload = {
        "username": "userone",
        "email": "duplicate@example.com",
        "password": "Password@123",
    }
    client.post("/api/v1/auth/register", json=payload)

    payload["username"] = "usertwo"
    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 409
    assert "email" in response.json()["detail"].lower()


def test_register_duplicate_username_returns_409(client):
    payload = {
        "username": "sameuser",
        "email": "one@example.com",
        "password": "Password@123",
    }
    client.post("/api/v1/auth/register", json=payload)

    payload["email"] = "two@example.com"
    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 409
    assert "username" in response.json()["detail"].lower()


def test_register_invalid_email_returns_422(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "johndoe",
            "email": "not-an-email",
            "password": "Password@123",
        },
    )

    assert response.status_code == 422


def test_register_weak_password_missing_uppercase_returns_422(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "johndoe",
            "email": "john@example.com",
            "password": "password@123",
        },
    )

    assert response.status_code == 422


def test_register_weak_password_missing_special_char_returns_422(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "johndoe",
            "email": "john@example.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 422


def test_register_password_too_short_returns_422(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "johndoe",
            "email": "john@example.com",
            "password": "Sh0rt@1",
        },
    )

    assert response.status_code == 422


def test_register_missing_required_fields_returns_422(client):
    response = client.post("/api/v1/auth/register", json={})

    assert response.status_code == 422


def test_register_username_too_short_returns_422(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "ab",
            "email": "john@example.com",
            "password": "Password@123",
        },
    )

    assert response.status_code == 422


def test_register_username_with_invalid_characters_returns_422(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "john doe!",
            "email": "john@example.com",
            "password": "Password@123",
        },
    )

    assert response.status_code == 422


def test_register_email_is_normalized_to_lowercase(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "johndoe",
            "email": "JOHN@EXAMPLE.COM",
            "password": "Password@123",
        },
    )

    assert response.status_code == 201
    assert response.json()["email"] == "john@example.com"
