from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserRegister
from app.core.security import hash_password
from app.core.exceptions import EmailAlreadyExistsError, UsernameAlreadyExistsError
from app.models.user import User


class AuthService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def register_user(self, data: UserRegister) -> User:
        if self.repository.get_by_email(data.email):
            raise EmailAlreadyExistsError("Email is already registered")

        if self.repository.get_by_username(data.username):
            raise UsernameAlreadyExistsError("Username is already taken")

        hashed_password = hash_password(data.password)

        user = self.repository.create_user(
            username=data.username,
            email=data.email,
            hashed_password=hashed_password,
        )
        return user