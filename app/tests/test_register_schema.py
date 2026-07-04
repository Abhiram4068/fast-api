import pytest
from pydantic import ValidationError

from app.schemas.auth import UserRegister


def test_valid_registration_schema():
    user = UserRegister(
        username="abhiram",
        email="abhiram@example.com",
        password="Password123",
    )

    assert user.username == "abhiram"
    assert user.email == "abhiram@example.com"


def test_invalid_email():
    with pytest.raises(ValidationError):
        UserRegister(
            username="abhiram",
            email="invalid-email",
            password="Password123",
        )


def test_short_password():
    with pytest.raises(ValidationError):
        UserRegister(
            username="abhiram",
            email="abhiram@example.com",
            password="123",
        )