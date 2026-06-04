import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.main import app
from src.app.config import settings
from src.app.database import get_db, Base
from src.app.oauth2 import create_access_token
from src.app import models


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_user}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def overrid_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = overrid_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "wed12345@gmail.com", "password": "pass234"}
    res = client.post("/users/", json=user_data)

    new_user = res.json()
    new_user["password"] = user_data["password"]

    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "wed123456789@gmail.com", "password": "pass234"}
    res = client.post("/users/", json=user_data)

    new_user = res.json()
    new_user["password"] = user_data["password"]

    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


@pytest.fixture
def test_posts(session, test_user, test_user2):
    post_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user["id"],
        },
        {
            "title": "second title",
            "content": "second content",
            "owner_id": test_user["id"],
        },
        {
            "title": "third title",
            "content": "third content",
            "owner_id": test_user["id"],
        },
        {
            "title": "third title",
            "content": "third content",
            "owner_id": test_user2["id"],
        },
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = list(map(create_post_model, post_data))

    session.add_all(post_map)
    session.commit()

    posts = session.query(models.Post).all()

    return posts
