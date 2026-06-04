"""
Handles all database connection and session management using SQLAlchemy.

This module defines the necessary components to connect to the PostgreSQL database,
create sessions for transactions, and provide a declarative base for the models.
It includes the `get_db` dependency, which is used across the application
to inject a database session into path operation functions.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from src.app.config import settings


# Construct the full database connection URL from the settings loaded from the .env file.
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_user}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"

# Create the main SQLAlchemy engine. This is the entry point to the database.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory. Each instance of SessionLocal will be a new database session.
# The session is not yet opened.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a declarative base class. All ORM models will inherit from this class.
Base = declarative_base()


def get_db():
    """
    FastAPI dependency that provides a database session for each request.

    This function is a generator that creates a new SessionLocal instance,
    yields it to the path operation function, and then ensures that the session
    is always closed, even if an error occurs during the request.

    Yields:
        Session: The SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
