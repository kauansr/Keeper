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
def created_product():
    """
    Fixture to create a product.

    Sends a POST request to create the Product and asserts success.
    Returns the created Product's ID and use for tests.
    """
    unique_id = 5
    data = {
        "name": "Product1",
        "fk_user": unique_id,
        "date_expire": "2025-09-25",
        "price": 154.44,
    }
    response = client.post("/product", json=data)
    assert response.status_code == 200
    return response.json()["id"], unique_id


def test_get_products():
    """
    Test retrieving a list of products.

    Sends a GET request to /product and asserts that the response status code
    is either 200 (OK) or 400 (Bad Request if no products exist).
    """
    response = client.get("/product")
    assert response.status_code in [200, 400]


def test_create_product():
    """
    Test product creation.

    Generates a product and sends a POST request to create a product.
    Asserts that the status code is 200 or 400.
    If successful, checks that the returned JSON contains the user ID.
    """
    unique_fk = 5
    data = {
        "name": "Product1",
        "fk_user": unique_fk,
        "date_expire": "2025-09-25",
        "price": 154.44,
    }
    response = client.post("/product", json=data)
    assert response.status_code in [200, 400]
    if response.status_code == 200:
        assert "fk_user" in response.json()


def test_update_product(created_product):
    """
    Test updating an existing product.

    Uses the 'created_product' fixture to get a valid product ID.
    Sends a PUT request to update the product's data.
    Asserts that the response status code is 200 or 400.
    """
    product_id, _ = created_product

    data = {
        "name": "product Atualizado",
        "price": 5.55555,
        "date_expire": "2025-09-29",
    }
    response = client.put(f"/product/update/{product_id}", json=data)
    assert response.status_code in [200, 400]


def test_delete_product(created_product):
    """
    Test deleting an existing product.

    Uses the 'created_Product' fixture to get a valid Product ID.
    Sends a DELETE request to remove the product.
    Asserts that the response status code is 200 or 400.
    """
    user_product, _ = created_product
    response = client.delete(f"/product/{user_product}")
    assert response.status_code in [200, 400]
