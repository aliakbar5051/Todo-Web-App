from pydantic import BaseModel, Field

from schemas.user import UserResponse


class LoginRequest(BaseModel):
    """Payload for POST /api/auth/login."""

    email: str = Field(min_length=1)
    password: str = Field(min_length=1)


class TokenResponse(BaseModel):
    """Response returned upon successful login."""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse
