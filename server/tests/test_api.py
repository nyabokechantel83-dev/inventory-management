import pytest
from app import app, inventory


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_get_inventory(client):
    response = client.get("/inventory")

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_get_one_item(client):
    response = client.get("/inventory/1")

    assert response.status_code == 200
    assert response.get_json()["id"] == 1


def test_get_missing_item(client):
    response = client.get("/inventory/999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Inventory item not found"


def test_create_item(client):
    response = client.post(
        "/inventory",
        json={
            "product_name": "Test Shirt",
            "brands": "Test Brand",
            "ingredients_text": "Cotton",
            "price": 800,
            "stock": 10
        }
    )

    assert response.status_code == 201
    assert response.get_json()["product_name"] == "Test Shirt"


def test_create_item_missing_name(client):
    response = client.post(
        "/inventory",
        json={
            "brands": "Test Brand",
            "price": 800,
            "stock": 10
        }
    )

    assert response.status_code == 400


def test_create_item_negative_price(client):
    response = client.post(
        "/inventory",
        json={
            "product_name": "Test Shirt",
            "brands": "Test Brand",
            "price": -100,
            "stock": 10
        }
    )

    assert response.status_code == 400


def test_update_item(client):
    response = client.patch(
        "/inventory/1",
        json={
            "price": 600,
            "stock": 20
        }
    )

    assert response.status_code == 200
    assert response.get_json()["price"] == 600
    assert response.get_json()["stock"] == 20


def test_update_missing_item(client):
    response = client.patch(
        "/inventory/999",
        json={
            "price": 600
        }
    )

    assert response.status_code == 404


def test_delete_item(client):
    original_length = len(inventory)

    response = client.delete("/inventory/2")

    assert response.status_code == 200
    assert len(inventory) == original_length - 1