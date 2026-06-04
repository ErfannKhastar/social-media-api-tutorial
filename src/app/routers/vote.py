"""
Defines the API router for handling votes on posts.

This module contains the endpoint for users to cast or remove a vote on a
specific post. The operations are protected and require user authentication.
"""

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(prefix="/votes", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Casts or removes a vote on a post for the authenticated user.

    The direction of the vote is controlled by the `dir` field in the request body:
    - `dir = 1`: Add a vote (upvote).
    - `dir = 0`: Remove a vote (downvote).

    A user cannot vote on the same post more than once.

    Args:
        vote (schemas.Vote): The request body containing the post_id and vote direction.
        db (Session): The database session dependency.
        current_user (models.User): The authenticated user making the request.

    Raises:
        HTTPException(404): If the post to be voted on does not exist.
        HTTPException(409): If the user tries to add a vote to a post they have already voted on.
        HTTPException(404): If the user tries to remove a vote that does not exist.

    Returns:
        dict: A success message indicating the action performed.
    """

    # Check if the post being voted on actually exists.
    post = db.query(models.Post.id).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=404, detail=f"Post with id {vote.post_id} does not exist"
        )

    # Query to find if a vote already exists from this user on this post.
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id
    )

    found_vote = vote_query.first()

    if vote.dir == 1:  # User wants to add a vote
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already voted on post {vote.post_id}",
            )

        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)

        db.add(new_vote)
        db.commit()

        return {"message": "successfully added vote"}

    else:  # User wants to remove a vote
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist"
            )

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}
