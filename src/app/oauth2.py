"""
Handles all OAuth2-related logic, including JWT token creation and verification.

This module provides the necessary functions to implement token-based authentication.
It defines the security scheme, creates access tokens for authenticated users,
and provides a dependency (`get_current_user`) to protect endpoints and retrieve
the currently logged-in user.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from src.app import schemas, database, models
from src.app.config import settings


# Define the OAuth2 password bearer scheme. The 'tokenUrl' points to the login endpoint.
# This tells FastAPI where clients should go to get a token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --- Security Constants ---
# Load sensitive data from the centralized settings management.
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    """
    Creates a new JWT access token.

    Args:
        data (dict): The payload data to encode within the token (e.g., user_id).

    Returns:
        str: The encoded JWT access token as a string.
    """
    to_encode = data.copy()

    # Set the token's expiration time.
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    # Encode the payload with the secret key and algorithm.
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    """
    Decodes and verifies a JWT access token.

    Args:
        token (str): The JWT token from the client's request.
        credentials_exception (HTTPException): The exception to raise if validation fails.

    Raises:
        credentials_exception: If the token is invalid, expired, or malformed.

    Returns:
        schemas.TokenData: The validated token data containing the user ID.
    """
    try:
        # Attempt to decode the token using the secret key and algorithm.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract the user ID from the payload.
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        # Validate the extracted data using the TokenData schema.
        token_data = schemas.TokenData(id=id)

    except JWTError:
        # If any error occurs during decoding, raise the credentials exception.
        raise credentials_exception

    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
):
    """
    FastAPI dependency to get the current authenticated user.

    This function is used in path operations to protect routes and identify the
    user making the request. It verifies the provided token and fetches the
    corresponding user from the database.

    Args:
        token (str): The bearer token extracted from the request's Authorization header.
        db (Session): The database session dependency.

    Returns:
        models.User: The SQLAlchemy User model for the authenticated user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_exception)

    # Fetch the user from the database using the ID from the token.
    user = db.query(models.User).filter(models.User.id == token.id).first()

    if user is None:
        # This is an extra security check in case the user was deleted after the token was issued.
        raise credentials_exception

    return user
