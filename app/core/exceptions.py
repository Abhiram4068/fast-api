class EmailAlreadyExistsError(Exception):
    """Raised when attempting to register with an email that already exists."""
    pass


class UsernameAlreadyExistsError(Exception):
    """Raised when attempting to register with a username that already exists."""
    pass


class UserNotFoundError(Exception):
    """Raised when a user cannot be found."""
    pass


class InvalidCredentialsError(Exception):
    """Raised when login credentials are invalid."""
    pass


class DepartmentNotFoundError(Exception):
    """Raised when a department cannot be found."""
    pass