from app.core.security import hash_password, verify_password


def test_hash_password_returns_different_string_than_plain():
    plain = "MyPassword@123"
    hashed = hash_password(plain)

    assert hashed != plain
    assert isinstance(hashed, str)


def test_hash_password_produces_different_hash_each_time():
    plain = "MyPassword@123"
    hash_one = hash_password(plain)
    hash_two = hash_password(plain)

    # bcrypt includes a random salt, so two hashes of the same password differ
    assert hash_one != hash_two


def test_verify_password_succeeds_with_correct_password():
    plain = "MyPassword@123"
    hashed = hash_password(plain)

    assert verify_password(plain, hashed) is True


def test_verify_password_fails_with_incorrect_password():
    hashed = hash_password("MyPassword@123")

    assert verify_password("WrongPassword@456", hashed) is False
