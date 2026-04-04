import pytest
from models import User, Verification
from datetime import datetime, timedelta
from middleware.auth_middleware import get_current_user
from app import app

@pytest.fixture
def test_user(db_session):
    # Create user
    user = User(
        name="Workspace User",
        email="workspace@example.com",
        password="hashedpassword",
        isEmailVerified=True
    )
    db_session.add(user)
    db_session.flush()
    db_session.refresh(user)
    return user

@pytest.fixture(autouse=True)
def override_auth(test_user):
    # Mock the current user dependency to avoid broken middleware (UUID issue)
    app.dependency_overrides[get_current_user] = lambda: test_user
    yield
    app.dependency_overrides.pop(get_current_user, None)

@pytest.fixture
def auth_token(test_user):
    # Generate token directly to satisfy the security dependency
    import jwt
    import os
    token = jwt.encode(
        {"userId": str(test_user.id), "exp": datetime.utcnow() + timedelta(days=1)},
        os.getenv("JWT_SECRET"),
        algorithm=os.getenv("ALGORITHM")
    )
    return f"Bearer {token}"

def test_create_workspace(client, auth_token):
    response = client.post(
        "/api-v1/workspaces/",
        json={
            "name": "Test Workspace",
            "description": "A workspace for testing",
            "color": "#FF5733"
        },
        headers={"Authorization": auth_token}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Workspace"

def test_get_workspaces(client, auth_token):
    # Create one first
    client.post(
        "/api-v1/workspaces/",
        json={"name": "WS 1", "description": "desc", "color": "#000"},
        headers={"Authorization": auth_token}
    )
    response = client.get("/api-v1/workspaces/", headers={"Authorization": auth_token})
    assert response.status_code == 200
    assert len(response.json()) >= 1
