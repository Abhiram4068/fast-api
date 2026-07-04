from app.repositories.user_repository import UserRepository


def test_get_by_email_returns_none_when_not_found(db_session):
    repo = UserRepository(db_session)

    result = repo.get_by_email("nonexistent@example.com")

    assert result is None


def test_get_by_username_returns_none_when_not_found(db_session):
    repo = UserRepository(db_session)

    result = repo.get_by_username("nonexistent_user")

    assert result is None


def test_create_user_persists_and_returns_user(db_session):
    repo = UserRepository(db_session)

    user = repo.create_user(
        username="johndoe",
        email="john@example.com",
        hashed_password="fake_hashed_value",
    )

    assert user.id is not None
    assert user.username == "johndoe"
    assert user.email == "john@example.com"
    assert user.hashed_password == "fake_hashed_value"
    assert user.is_active is True


def test_get_by_email_finds_created_user(db_session):
    repo = UserRepository(db_session)
    repo.create_user(
        username="janedoe",
        email="jane@example.com",
        hashed_password="fake_hashed_value",
    )

    found = repo.get_by_email("jane@example.com")

    assert found is not None
    assert found.username == "janedoe"


def test_get_by_username_finds_created_user(db_session):
    repo = UserRepository(db_session)
    repo.create_user(
        username="janedoe",
        email="jane@example.com",
        hashed_password="fake_hashed_value",
    )

    found = repo.get_by_username("janedoe")

    assert found is not None
    assert found.email == "jane@example.com"
