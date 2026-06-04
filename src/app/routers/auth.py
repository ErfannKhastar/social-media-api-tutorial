"""
Defines the authentication router for the application.

This module contains the path operation for user login. It handles the
OAuth2 password request flow, verifies user credentials, and returns a
JWT access token upon successful authentication.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth2


router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Authenticates a user and returns an access token.

    This endpoint follows the OAuth2 password flow. It expects a form-data
    body with 'username' (which is the user's email) and 'password'.

    Args:
        user_credentials (OAuth2PasswordRequestForm): The user's login credentials
            injected by FastAPI from the request form body.
        db (Session): The database session dependency.

    Raises:
        HTTPException(422): If username or password are not provided.
        HTTPException(403): If the credentials are invalid or incorrect.

    Returns:
        schemas.Token: An object containing the JWT access token and token type.
    """

    if not user_credentials.username or not user_credentials.password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Username and password must be provided",
        )

    # Note: In OAuth2PasswordRequestForm, the 'username' field is used for the email.
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    # Check if the user exists and if the password is correct.
    if not user or not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )

    # Create a new access token for the authenticated user.
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
