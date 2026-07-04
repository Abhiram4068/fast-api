import pytest

from app.services.auth_service import AuthService
from app.schemas.auth import UserRegister
from app.core.exceptions import EmailAlreadyExistsError, UsernameAlreadyExistsError


def make_register_payload(username="johndoe", email="john@example.com", password="Password@123"):
    return UserRegister(username=username, email=email, password=password)


def test_register_user_success(db_session):
    service = AuthService(db_session)
    payload = make_register_payload()

    user = service.register_user(payload)

    assert user.username == "johndoe"
    assert user.email == "john@example.com"
    assert user.hashed_password != "Password@123"  # must be hashed, not plaintext


def test_register_user_raises_on_duplicate_email(db_session):
    service = AuthService(db_session)
    service.register_user(make_register_payload(username="user1", email="dup@example.com"))

    with pytest.raises(EmailAlreadyExistsError):
        service.register_user(make_register_payload(username="user2", email="dup@example.com"))


def test_register_user_raises_on_duplicate_username(db_session):
    service = AuthService(db_session)
    service.register_user(make_register_payload(username="dupuser", email="a@example.com"))

    with pytest.raises(UsernameAlreadyExistsError):
        service.register_user(make_register_payload(username="dupuser", email="b@example.com"))
