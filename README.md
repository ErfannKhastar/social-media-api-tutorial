# FastAPI Social Media API

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-green.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blueviolet.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A complete, production-ready RESTful API for a simple social media application built with FastAPI, PostgreSQL, and Docker. This project includes user authentication with JWT, full CRUD operations for posts, and a voting system.

## About The Project

This project serves as a comprehensive example of building a modern web API using Python. It was developed as a learning exercise but is structured to follow professional best practices, including database migrations with Alembic, dependency management, and containerization with Docker and Docker Compose for both development and production environments.

## Features

-   **User Authentication**: User registration and login with JWT token authentication.
-   **Password Hashing**: Secure password storage using `passlib` and bcrypt.
-   **Post Management**: Full CRUD (Create, Read, Update, Delete) functionality for user posts.
-   **Voting System**: Users can upvote posts (one vote per user per post).
-   **Database Migrations**: Schema management using Alembic.
-   **Containerized**: Fully containerized with Docker for consistent development and production environments.
-   **Dependency Injection**: Utilizes FastAPI's dependency injection system for database sessions and user authentication.
-   **Auto-generated Documentation**: Interactive API documentation available via Swagger UI (`/docs`) and ReDoc (`/redoc`).

## Tech Stack

-   **Backend**: Python, FastAPI
-   **Database**: PostgreSQL
-   **ORM**: SQLAlchemy
-   **Migrations**: Alembic
-   **Containerization**: Docker, Docker Compose
-   **Data Validation**: Pydantic
-   **Authentication**: python-jose, passlib

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

-   Git
-   Python 3.9+
-   Docker Desktop (for Docker methods)
-   A running local instance of PostgreSQL (for the non-Docker local method)

### Configuration

1.  Clone the repository:
    ```sh
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```
2.  Create a `.env` file in the root of the project. Copy the content below into the file and replace the placeholder values with your own settings.

    ```env
    # Application Settings
    SECRET_KEY=your_super_secret_key_here
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30

    # Database Settings for the API
    DATABASE_HOST=localhost # Use 'postgres' when running with Docker
    DATABASE_PORT=5432
    DATABASE_USER=your_db_user
    DATABASE_PASSWORD=your_db_password
    DATABASE_NAME=your_db_name

    # Initial settings for the Postgres Docker container
    # These values should match the ones above
    POSTGRES_PASSWORD=your_db_password
    POSTGRES_DB=your_db_name
    ```

## Installation & Running

There are three ways to run this application:

### Option 1: Local Development (Without Docker)

This method is for running the app directly on your machine using a Python virtual environment and a local PostgreSQL server.

1.  **Create and activate a virtual environment:**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```
2.  **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
3.  **Configure your `.env` file:**
    Make sure `DATABASE_HOST` is set to `localhost`.
4.  **Apply database migrations:**
    Ensure your local PostgreSQL server is running, then run:
    ```sh
    alembic upgrade head
    ```
5.  **Run the application:**
    ```sh
    uvicorn app.main:app --reload
    ```
    The API will be available at `http://localhost:8000`.

### Option 2: Docker - Development Mode (From Source Code)

This is the recommended method for development. It uses Docker Compose to build and run the application and database containers.

1.  **Configure your `.env` file:**
    Make sure `DATABASE_HOST` is set to `postgres`.
2.  **Build and run the containers:**
    ```sh
    docker compose -f docker-compose-dev.yml up -d --build
    ```
3.  **Apply database migrations:**
    After the containers are up and running, execute the following command to create the database tables:
    ```sh
    docker compose -f docker-compose-dev.yml exec api python -m alembic upgrade head
    ```
    The API will be available at `http://localhost:8000`.

### Option 3: Docker - Production Mode (From Pre-built Image)

This method simulates a production environment by running the application from a pre-built Docker image.

1.  **Ensure the image exists:**
    This method assumes that an image `erfannkhastarr/fastapi-crud-tutorial:latest` has been pushed to a Docker registry.
2.  **Configure your `.env` file:**
    Make sure `DATABASE_HOST` is set to `postgres`.
3.  **Run the containers:**
    ```sh
    docker compose --env-file .env -f docker-compose-prod.yml up -d
    ```
4.  **Apply database migrations:**
    Once the containers are running, apply the database migrations:
    ```sh
    docker compose --env-file .env -f docker-compose-prod.yml exec api python -m alembic upgrade head
    ```
    The API will be available on port 80, so you can access it at `http://localhost`.

## API Usage

Once the application is running, you can access the interactive API documentation (Swagger UI) at:

**`http://localhost:8000/docs`** (for development mode)

**`http://localhost/docs`** (for production mode)

From there, you can explore all the available endpoints, see the required schemas, and test the API directly from your browser.