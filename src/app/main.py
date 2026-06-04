"""
Main module and entrypoint for the FastAPI application.

This file is responsible for the following:
- Creating the main FastAPI application instance.
- Configuring and adding CORS (Cross-Origin Resource Sharing) middleware.
- Including all the routers from different parts of the application.
- Defining a root endpoint ("/") for health checks and a welcome message.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.routers import post, user, auth, vote

# Create the main FastAPI application instance
app = FastAPI(
    title="Social Media API",
    description="A complete API for a simple social media platform, featuring posts, users, voting, and authentication.",
)

# A list of allowed origins for CORS. "*" allows all origins.
# For a production environment, it's recommended to replace "*" with the specific
# frontend URL (e.g., "https://www.your-frontend.com").
origins = ["*"]

# Add the CORS middleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers for each section of the application
app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    """
    The root endpoint of the application.

    This endpoint serves as a health check. A successful response from this
    endpoint indicates that the application is running correctly.

    Returns:
        dict: A simple welcome message.
    """
    return {"message": "Hello World, welcome to my FastAPI application!"}
