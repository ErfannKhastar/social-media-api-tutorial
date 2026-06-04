"""
Defines the SQLAlchemy ORM models for the application.

These classes map to the tables in the database. Each class represents a table,
and each attribute of the class represents a column in that table. SQLAlchemy's
ORM uses these models to interact with the database in an object-oriented way.
"""

from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship
from src.app.database import Base


class Post(Base):
    """
    Represents a post in the 'posts' table.
    """

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default="True")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    # Foreign key to the 'users' table. 'CASCADE' ensures that if a user is
    # deleted, all their posts are also deleted.
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    # Create a relationship to the User model. This allows SQLAlchemy to
    # automatically fetch the owner of a post.
    owner = relationship("User")


class User(Base):
    """
    Represents a user in the 'users' table.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Vote(Base):
    """
    Represents a vote on a post by a user in the 'votes' table.

    This model defines a many-to-many relationship between users and posts,
    using a composite primary key made of user_id and post_id.
    """

    __tablename__ = "votes"

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    post_id = Column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True,
    )
