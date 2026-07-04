from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from app.core.exceptions import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    UsernameAlreadyExistsError,
)
from app.models.user import User
from app.repositories.token_blacklist_repository import TokenBlacklistRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserLogin, UserRegister


class AuthService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
        self.blacklist_repo = TokenBlacklistRepository(db)

    # ------------------------------------------------------------------ #
    # Registration
    # ------------------------------------------------------------------ #
    def register_user(self, data: UserRegister) -> User:
        if self.repository.get_by_email(data.email):
            raise EmailAlreadyExistsError("Email is already registered")

        if self.repository.get_by_username(data.username):
            raise UsernameAlreadyExistsError("Username is already taken")

        hashed = hash_password(data.password)
        return self.repository.create_user(
            username=data.username,
            email=data.email,
            hashed_password=hashed,
        )

    # ------------------------------------------------------------------ #
    # Authentication
    # ------------------------------------------------------------------ #
    def authenticate_user(self, data: UserLogin) -> User:
        user = self.repository.get_by_email(data.email)
        if not user or not verify_password(data.password, user.hashed_password):
            raise InvalidCredentialsError("Invalid email or password")
        return user

    def create_tokens_for_user(self, user: User) -> tuple[str, str]:
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        return access_token, refresh_token

    # ------------------------------------------------------------------ #
    # Token blacklist
    # ------------------------------------------------------------------ #
    def logout_user(self, access_token: str, refresh_token: str) -> None:
        """
        Revokes both the access token and the refresh token so they
        cannot be used again even if an attacker captured them.
        """
        for token in (access_token, refresh_token):
            if not token:
                continue
            try:
                payload = decode_access_token(token)
                # exp is a Unix timestamp (int) — convert to aware datetime
                expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
            except (ValueError, KeyError):
                # Malformed / expired token — no need to store it
                continue
            self.blacklist_repo.blacklist_token(token=token, expires_at=expires_at)

    def is_token_blacklisted(self, token: str) -> bool:
        return self.blacklist_repo.is_blacklisted(token)