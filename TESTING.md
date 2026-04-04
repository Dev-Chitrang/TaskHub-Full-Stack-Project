# Testing Documentation

## Overview
TaskHub uses `pytest` for backend testing. The goal is to verify the API endpoints, business logic, and database interactions.

## Setup
To run tests locally, ensure you have installed the backend dependencies:
```bash
cd backend
pip install -r requirements.txt
pip install pytest httpx
```

## Running Tests
Run all tests using the following command:
```bash
cd backend
pytest tests/
```

## Test Structure
- `conftest.py`: Contains global fixtures like the test database engine, session, and `TestClient`.
- `test_auth.py`: Tests user registration, email verification, and login.
- `test_workspace.py`: Tests workspace creation and retrieval.

## Strategy
- **Isolation**: Each test runs in its own database transaction and is rolled back after completion to ensure no side effects.
- **Mocking**: External services like email validation and background tasks are mocked to avoid dependencies on internet access or real SMTP servers.
- **Authentication**: Helper fixtures provide valid JWT tokens for authenticated requests.

## Continuous Integration
Tests are automatically run on every push and pull request to the `main` or `master` branches via GitHub Actions.
Check `.github/workflows/ci.yml` for the CI configuration.
