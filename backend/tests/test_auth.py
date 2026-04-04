import pytest
from unittest.mock import patch

@pytest.fixture(autouse=True)
def mock_email_check():
    with patch("routes.auth.full_email_check") as mock:
        mock.return_value = []
        yield mock

@pytest.fixture(autouse=True)
def mock_background_tasks():
    with patch("fastapi.BackgroundTasks.add_task") as mock:
        yield mock

def test_register_user(client):
    response = client.post(
        "/api-v1/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
            "is2FAEnabled": False
        }
    )
    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully"

def test_register_duplicate_user(client):
    payload = {
        "name": "Test User",
        "email": "duplicate@example.com",
        "password": "password123",
        "is2FAEnabled": False
    }
    client.post("/api-v1/auth/register", json=payload)
    response = client.post("/api-v1/auth/register", json=payload)
    assert response.status_code == 400
    assert response.json()["message"] == "User already exists"

def test_login_unverified_user(client):
    # Register user
    client.post(
        "/api-v1/auth/register",
        json={
            "name": "Unverified User",
            "email": "unverified@example.com",
            "password": "password123",
            "is2FAEnabled": False
        }
    )
    # Attempt login
    response = client.post(
        "/api-v1/auth/login",
        json={
            "email": "unverified@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 401
    assert response.json()["message"] == "Please verify your email first"
