"""
Contains utility functions for the application.

This module provides common, reusable functions that don't belong to a
specific business logic domain, such as password hashing and verification.
"""

from passlib.context import CryptContext


# Create a CryptContext instance, specifying bcrypt as the hashing algorithm.
# 'deprecated="auto"' automatically handles updates to the hashing scheme.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    """
    Hashes a plain-text password using the bcrypt algorithm.

    Args:
        password (str): The plain-text password to hash.

    Returns:
        str: The resulting hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """
    Verifies a plain-text password against a stored hashed password.

    Args:
        plain_password (str): The plain-text password from a user login attempt.
        hashed_password (str): The hashed password stored in the database.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)
