"""
Defines the Pydantic models (schemas) for the application.

These schemas are used for:
1.  Data validation for incoming request bodies.
2.  Data serialization for outgoing responses.
3.  Generating the OpenAPI (Swagger UI) documentation.

Separating schemas from the database models provides a clear and secure API layer.
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional, Annotated


# --- User Schemas ---


class UserCreate(BaseModel):
    """Schema for data required to create a new user."""

    email: EmailStr
    password: str


class UserOut(BaseModel):
    """Schema for data returned to the client when a user is retrieved.

    This schema intentionally omits sensitive information like the password.
    """

    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    # Pydantic's 'from_attributes = True' allows it to read data from ORM models.


class UserLogin(BaseModel):
    """Schema for user login credentials."""

    email: EmailStr
    password: str


# --- Post Schemas ---


class PostBase(BaseModel):
    """Base schema for a post, containing common attributes."""

    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    """Schema for creating a new post. Inherits all fields from PostBase."""

    pass


class Post(PostBase):
    """
    Schema representing a complete post as it is stored in the database.
    Used for responses that should include all post details and owner info.
    """

    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut  # Nested Pydantic model to include owner's public info.

    model_config = ConfigDict(from_attributes=True)


class PostOut(BaseModel):
    """Specialized schema for returning a post along with its vote count."""

    Post: Post
    votes: int

    model_config = ConfigDict(from_attributes=True)


# --- Token Schemas ---


class Token(BaseModel):
    """Schema for the JWT access token returned upon successful login."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for the data embedded within a JWT access token (the payload)."""

    id: Optional[int] = None


# --- Vote Schema ---


class Vote(BaseModel):
    """Schema for casting a vote."""

    post_id: int
    # The direction of the vote. Annotated is used for extra validation.
    # ge=0 means 'greater than or equal to 0'
    # le=1 means 'less than or equal to 1'
    dir: Annotated[int, Field(strict=True, ge=0, le=1)]
