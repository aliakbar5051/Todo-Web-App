from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from core.security import hash_password, verify_password
from models.user import User
from schemas.user import UserRegister


def register_user(db: Session, data: UserRegister) -> User:
    """Register a new user after verifying unique email and hashing password."""
    # Check if email is already taken (case-insensitive)
    existing_stmt = select(User).where(func.lower(User.email) == data.email.lower())
    existing_user = db.scalar(existing_stmt)
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email address already exists.",
        )

    # Hash the password securely with Argon2
    hashed = hash_password(data.password)

    user = User(
        name=data.name,
        email=data.email.lower(),
        password_hash=hashed,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User:
    """Verify credentials and return user.
    
    Uses a generic error message to prevent email enumeration.
    """
    clean_email = email.strip().lower()
    stmt = select(User).where(func.lower(User.email) == clean_email)
    user = db.scalar(stmt)

    if user is None or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
