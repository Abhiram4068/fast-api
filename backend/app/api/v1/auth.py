from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.core.security import create_access_token, decode_access_token
from app.core.exceptions import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    UsernameAlreadyExistsError,
)
from app.database.session import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserLogin, UserRegister, RegisterResponse, LoginResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


# ------------------------------------------------------------------ #
# Register
# ------------------------------------------------------------------ #
@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    service = AuthService(db)
    try:
        user = service.register_user(payload)
    except EmailAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except UsernameAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    return RegisterResponse(id=user.id, username=user.username, email=user.email)


# ------------------------------------------------------------------ #
# Login
# ------------------------------------------------------------------ #
@router.post("/login", response_model=LoginResponse)
def login(payload: UserLogin, response: Response, db: Session = Depends(get_db)):
    service = AuthService(db)
    try:
        user = service.authenticate_user(payload)
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    access_token, refresh_token = service.create_tokens_for_user(user)
    _set_auth_cookies(response, access_token, refresh_token)

    return LoginResponse(id=user.id, username=user.username, email=user.email)


# ------------------------------------------------------------------ #
# Refresh
# ------------------------------------------------------------------ #
@router.post("/refresh")
def refresh(request: Request, response: Response, db: Session = Depends(get_db)):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No refresh token"
        )

    try:
        payload = decode_access_token(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type"
        )

    # Reject revoked refresh tokens
    service = AuthService(db)
    if service.is_token_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has been revoked"
        )

    user_id = payload.get("sub")
    user = UserRepository(db).get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    new_access_token = create_access_token(data={"sub": str(user.id)})
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )
    return {"message": "Access token refreshed"}


# ------------------------------------------------------------------ #
# Logout
# ------------------------------------------------------------------ #
@router.post("/logout")
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    # Blacklist whichever tokens we can read from the cookies
    service = AuthService(db)
    service.logout_user(
        access_token=access_token or "",
        refresh_token=refresh_token or "",
    )

    # Clear cookies client-side as well
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/api/v1/auth")
    return {"message": "Logged out successfully"}


# ------------------------------------------------------------------ #
# Helpers
# ------------------------------------------------------------------ #
def _set_auth_cookies(response: Response, access_token: str, refresh_token: str):
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/api/v1/auth",  # scoped to all auth routes so logout can also read it
    )