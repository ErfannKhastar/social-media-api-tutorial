import pytest
from jose import jwt
from src.app import schemas
from src.app.config import settings


def test_root(client):
    res = client.get("/")
    assert (
        res.json().get("message") == "Hello World, welcome to my FastAPI application!"
    )


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "wed12345@gmail.com", "password": "pass234"}
    )
    new_user = schemas.UserOut(**res.json())

    assert res.status_code == 201
    assert new_user.email == "wed12345@gmail.com"


def test_login_user(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )

    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )

    id = payload.get("user_id")

    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "pass123", 403),
        ("asdfg@gmail.com", "pass123", 403),
        ("erfan@gmail.com", "wrongpass", 403),
        (None, "wrongpass123", 422),
        ("pass123@gmail.com", None, 422),
    ],
)
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post(
        "/login",
        data={"username": email, "password": password},
    )

    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid credentials"
