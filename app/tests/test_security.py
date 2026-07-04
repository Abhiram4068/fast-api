from app.core.settings import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_hash_password():
    password = "Password123"

    hashed = hash_password(password)

    assert hashed != password
    assert isinstance(hashed, str)


def test_verify_correct_password():
    password = "Password123"

    hashed = hash_password(password)

    assert verify_password(password, hashed) is True


def test_verify_wrong_password():
    password = "Password123"

    hashed = hash_password(password)

    assert verify_password("WrongPassword", hashed) is False


def test_create_access_token():
    token = create_access_token(
        {"sub": "abhiram@example.com"}
    )

    assert isinstance(token, str)
    assert len(token) > 20


def test_decode_access_token():
    token = create_access_token(
        {"sub": "abhiram@example.com"}
    )

    payload = decode_access_token(token)

    assert payload["sub"] == "abhiram@example.com"
    assert "exp" in payload