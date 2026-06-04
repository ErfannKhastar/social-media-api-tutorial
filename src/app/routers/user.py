"""
Defines the API router for user-related operations.

This module contains endpoints for user creation (registration) and retrieval
of public user information.
"""

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Creates a new user in the database (user registration).

    The user's password is hashed before being stored for security.

    Args:
        user (schemas.UserCreate): The user data (email and password) from the request body.
        db (Session): The database session dependency.

    Raises:
        HTTPException: If a user with the same email already exists (handled by the database unique constraint).

    Returns:
        schemas.UserOut: The newly created user's public information (excluding the password).
    """

    # Hash the password before storing it in the database.
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    """
    Retrieves a specific user by their unique ID.

    Args:
        id (int): The ID of the user to retrieve.
        db (Session): The database session dependency.

    Raises:
        HTTPException(404): If a user with the specified ID is not found.

    Returns:
        schemas.UserOut: The requested user's public information.
    """

    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {id} was not found",
        )

    return user
