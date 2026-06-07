# FastAPI Social Media API

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-green.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blueviolet.svg)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-success)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A complete, production-ready RESTful API for a simple social media application built with FastAPI, PostgreSQL, and Docker. This project includes user authentication with JWT, full CRUD operations for posts, an automated testing pipeline, and a voting system.

## 🚀 About The Project

This project serves as a comprehensive example of building a modern web API using Python. It is structured to follow professional software engineering best practices, including database migrations with Alembic, dependency management, automated CI/CD pipelines, and containerization with Docker and Docker Compose for both development and production environments.

## ✨ Features

- **User Authentication**: User registration and secure login using OAuth2 and JWT tokens.
- **Password Hashing**: Secure password storage using `passlib` and bcrypt.
- **Post Management**: Full CRUD (Create, Read, Update, Delete) functionality for user posts.
- **Voting System**: Users can upvote/downvote posts (limited to one vote per user per post).
- **Database Migrations**: Schema management and version control using Alembic.
- **Automated Testing**: Comprehensive unit testing using `pytest`.
- **CI/CD Pipeline**: Fully automated integration and deployment workflow via GitHub Actions (auto-tests & Docker Hub pushes).
- **Containerization**: Fully containerized with Docker for consistent development and production setups.
- **Auto-generated Documentation**: Interactive API documentation available via Swagger UI (`/docs`) and ReDoc (`/redoc`).

## 🛠 Tech Stack

- **Backend**: Python 3.11, FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Testing**: Pytest
- **Containerization**: Docker, Docker Compose
- **Data Validation**: Pydantic
- **Authentication**: python-jose, passlib

## 🏁 Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

- Git
- Python 3.11+
- Docker & Docker Compose (for Dockerized environments)
- A local instance of PostgreSQL (only if running without Docker)

### Configuration

1. Clone the repository:
   ```sh
   git clone [https://github.com/erfankhastar/social_media_api_tutorial.git](https://github.com/erfankhastar/social_media_api_tutorial.git)
   cd social_media_api_tutorial
   ```
2. Create a `.env` file in the root directory and copy the contents below (replace placeholders with your actual secrets):

   ```env
   # Application Settings
   SECRET_KEY=your_super_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30

   # Database Settings for the API
   DATABASE_HOST=localhost # Note: Use 'postgres' when running via Docker
   DATABASE_PORT=5432
   DATABASE_USER=postgres
   DATABASE_PASSWORD=your_db_password
   DATABASE_NAME=fastapi
   ```

## 💻 Installation & Running

There are three ways to run this application:

### Option 1: Local Development (Without Docker)

Ideal for direct script execution using a Python virtual environment.

1. **Create and activate a virtual environment:**
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Apply database migrations:**
   Ensure your local PostgreSQL server is running and `DATABASE_HOST` is `localhost`, then run:
   ```sh
   alembic upgrade head
   ```
4. **Run the application:**
   ```sh
   uvicorn src.app.main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

### Option 2: Docker - Development Mode (Live Reload)

The recommended method for local development. It maps your source code to the container, enabling live reloading.

1. Configure your `.env` file and set `DATABASE_HOST=postgres`.
2. **Build and run the containers:**
   ```sh
   docker-compose -f docker-compose-dev.yml up -d --build
   ```
3. **Apply database migrations inside the container:**
   ```sh
   docker-compose -f docker-compose-dev.yml exec api alembic upgrade head
   ```
   The API will be available at `http://localhost:8000`.

### Option 3: Docker - Production Mode

Simulates a production environment by pulling the pre-built, tested Docker image directly from Docker Hub.

1. Ensure `DATABASE_HOST=postgres` in your `.env` file.
2. **Run the containers:**
   ```sh
   docker-compose -f docker-compose-prod.yml up -d
   ```
3. **Apply database migrations:**
   ```sh
   docker-compose -f docker-compose-prod.yml exec api alembic upgrade head
   ```
   The API will be available on port 80 at `http://localhost`.

## 📚 API Documentation

Once the application is running, you can access the interactive API documentation at:
- **Development Mode:** `http://localhost:8000/docs`
- **Production Mode:** `http://localhost/docs`

## 🤝 Support & Contribution

If this project helped you understand FastAPI, Docker, or CI/CD pipelines better, please consider giving it a ⭐️! It helps others discover the repository and motivates me to keep building and sharing high-quality backend projects.

Contributions, issues, and feature requests are always welcome! 

## 📫 Let's Connect!

I'm a backend software engineer passionate about building scalable architectures, clean code, and robust APIs. Whether you have a question about this project, want to discuss Python backend development, or have an exciting collaboration in mind, I'd love to hear from you!

- 💻 **Explore my work:** [Check out my GitHub Profile](https://github.com/erfannkhastar) to see my backend journey and other projects.
- 🚀 **Project Link:** [FastAPI Social Media API](https://github.com/erfankhastar/social_media_api_tutorial)

## 📝 License

This project is distributed under the MIT License. See the [LICENSE](LICENSE) file for more details.
