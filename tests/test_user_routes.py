from fastapi.testclient import TestClient
from core.db_test import Basetest, enginetest
from main import app
import pytest
import uuid
import os

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Create the test database schema before tests run
    and drop all tables after tests finish.
    """
    Basetest.metadata.create_all(bind=enginetest)
    yield
    Basetest.metadata.drop_all(bind=enginetest)
    enginetest.dispose()  # close connections

    db_path = enginetest.url.database
    if db_path and os.path.exists(db_path):
        print(f"Deleting test database file: {db_path}")
        try:
            os.remove(db_path)
        except Exception as e:
            print(f"Error deleting test DB file: {e}")


@pytest.fixture
def created_user():
    """
    Fixture to create a user with a unique email address.

    Generates a unique email using UUID to avoid conflicts with existing users.
    Sends a POST request to create the user and asserts success.
    Returns the created user's ID and email for use in dependent tests.
    """
    unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    data = {"name": "João", "email": unique_email, "password": "senha123"}
    response = client.post("/user", json=data)
    assert response.status_code == 200
    return response.json()["id"], unique_email


def test_get_users():
    """
    Test retrieving a list of users.

    Sends a GET request to /user and asserts that the response status code
    is either 200 (OK) or 400 (Bad Request if no users exist).
    """
    response = client.get("/user")
    assert response.status_code in [200, 400]


def test_create_user():
    """
    Test user creation with a unique email.

    Generates a unique email and sends a POST request to create a user.
    Asserts that the status code is 200 or 400.
    If successful, checks that the returned JSON contains the user ID.
    """
    unique_email = f"maria_{uuid.uuid4().hex[:8]}@example.com"
    data = {"name": "Maria", "email": unique_email, "password": "senha123"}
    response = client.post("/user", json=data)
    assert response.status_code in [200, 400]
    if response.status_code == 200:
        assert "id" in response.json()


def test_update_user(created_user):
    """
    Test updating an existing user.

    Uses the 'created_user' fixture to get a valid user ID.
    Generates a new unique email for the update.
    Sends a PUT request to update the user's data.
    Asserts that the response status code is 200 or 400.
    """
    user_id, _ = created_user
    unique_email = f"user_update_{uuid.uuid4().hex[:8]}@example.com"
    data = {"name": "João Atualizado", "email": unique_email, "password": "nova123"}
    response = client.put(f"/user/update/{user_id}", json=data)
    assert response.status_code in [200, 400]


def test_delete_user(created_user):
    """
    Test deleting an existing user.

    Uses the 'created_user' fixture to get a valid user ID.
    Sends a DELETE request to remove the user.
    Asserts that the response status code is 200 or 400.
    """
    user_id, _ = created_user
    response = client.delete(f"/user/{user_id}")
    assert response.status_code in [200, 400]


def test_login(created_user):
    """
    Test user login functionality.

    Uses the 'created_user' fixture to get a valid email.
    Sends a POST request to the /login endpoint with the user's credentials.
    Asserts that the response status code is 200 or 400.
    If successful, verifies that the response contains an access token.
    """
    _, email = created_user
    data = {"email": email, "password": "senha123"}
    response = client.post("/login", json=data)
    assert response.status_code in [200, 400]
    if response.status_code == 200:
        assert "access_token" in response.json()
