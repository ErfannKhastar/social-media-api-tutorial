"""
Defines the API router for all post-related operations.

This module contains endpoints for creating, retrieving (single and multiple),
updating, and deleting posts. All endpoints are protected and require an
authenticated user.
"""

from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    """
    Retrieves a list of all posts with their corresponding vote counts.

    This endpoint supports pagination via `limit` and `skip` query parameters,
    and searching by post title using the `search` query parameter.

    Args:
        db (Session): The database session dependency.
        current_user (int): The authenticated user, injected by the oauth2 dependency.
        limit (int): The maximum number of posts to return.
        skip (int): The number of posts to skip for pagination.
        search (str, optional): A search term to filter posts by title.

    Returns:
        List[schemas.PostOut]: A list of posts, where each item contains the
                               post details and its total vote count.
    """

    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .order_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Creates a new post for the currently authenticated user.

    The new post is automatically associated with the user who is making the request.

    Args:
        post (schemas.PostCreate): The post data from the request body.
        db (Session): The database session dependency.
        current_user (models.User): The authenticated user object.

    Returns:
        models.Post: The newly created post, matching the `Post` schema.
    """
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Retrieves a single post by its ID, including its vote count.

    Args:
        id (int): The ID of the post to retrieve.
        db (Session): The database session dependency.
        current_user (models.User): The authenticated user object.

    Raises:
        HTTPException(404): If a post with the specified ID is not found.

    Returns:
        schemas.PostOut: The requested post details along with its vote count.
    """
    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} was not found",
        )

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Deletes a post by its ID.

    A user can only delete their own posts. This endpoint returns a 204 No Content
    status on successful deletion.

    Args:
        id (int): The ID of the post to delete.
        db (Session): The database session dependency.
        current_user (models.User): The authenticated user object.

    Raises:
        HTTPException(404): If the post with the specified ID does not exist.
        HTTPException(403): If the user is not the owner of the post.
    """

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} was not found",
        )

    # Authorization check: Ensure the user deleting the post is the owner.
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the owner of the post",
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Updates a post by its ID.

    A user can only update their own posts.

    Args:
        id (int): The ID of the post to update.
        updated_post (schemas.PostCreate): The updated post data from the request body.
        db (Session): The database session dependency.
        current_user (models.User): The authenticated user object.

    Raises:
        HTTPException(404): If the post with the specified ID does not exist.
        HTTPException(403): If the user is not the owner of the post.

    Returns:
        models.Post: The updated post.
    """

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} was not found",
        )

    # Authorization check: Ensure the user updating the post is the owner.
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the owner of the post",
        )

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()
