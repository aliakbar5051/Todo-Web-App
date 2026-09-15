from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.security import create_access_token
from database import get_db
from dependencies.auth import get_current_user
from models.user import User
from schemas.auth import LoginRequest, TokenResponse
from schemas.user import UserRegister, UserResponse
from services import auth_service

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    """Create a new user account with hashed password."""
    return auth_service.register_user(db, payload)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Log in and obtain JWT access token",
)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate with email and password, returning JWT access token."""
    user = auth_service.authenticate_user(db, payload.email, payload.password)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email}
    )
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current logged in user details",
)
def get_me(current_user: User = Depends(get_current_user)):
    """Return the profile of the currently authenticated user."""
    return current_user
