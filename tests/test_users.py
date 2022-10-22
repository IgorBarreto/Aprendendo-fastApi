from fastapi.testclient import TestClient
from fastapi import status, HTTPException

from pytest import raises
from app.main import app
from app.schemas import User

client = TestClient(app)


def test_root():
    res = client.get("/")
    assert res.json().get("message") == "Hello world!!"


def test_root_status_code_200():
    res = client.get("/")
    assert res.status_code == status.HTTP_200_OK


def test_create_user():
    res = client.post(
        "/users/", json={"email": "igorteste@gmail.com", "password": "senha123"}
    )
    new_user = User(**res.json())
    id = res.json().get("id")
    assert res.status_code == status.HTTP_201_CREATED
    assert new_user.email == "igorteste@gmail.com"
    client.delete(f"/users/{id}")


def test_email_alread_exists():
    res = client.post(
        "/users/", json={"email": "igorteste@gmail.com", "password": "senha123"}
    )
    id = res.json().get("id")
    res = client.post(
        "/users/", json={"email": "igorteste@gmail.com", "password": "senha123"}
    )
    assert res.status_code == status.HTTP_409_CONFLICT
    assert res.json().get("detail") == "Email already exists"
    client.delete(f"/users/{id}")


def test_user_login():
    res = client.post("/login", data={"username": "igor@gmail.com", "email": "pass"})

    assert res.status_code == status.HTTP_200_OK
