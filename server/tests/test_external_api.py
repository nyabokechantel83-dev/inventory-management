from unittest.mock import patch, Mock

from app import app, inventory, fetch_open_food_facts


def test_fetch_open_food_facts():
    with patch("app.requests.get") as mock_get:
        mock_response = Mock()

        mock_response.json.return_value = {
            "product": {
                "product_name": "Nutella",
                "brands": "Nutella, Ferrero",
                "ingredients_text": "Sugar, palm oil, hazelnuts"
            }
        }

        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        product = fetch_open_food_facts("3017620422003")

        assert product["product_name"] == "Nutella"
        assert product["brands"] == "Nutella, Ferrero"
        assert product["ingredients_text"] == "Sugar, palm oil, hazelnuts"

        mock_get.assert_called_once()


def test_get_external_product():
    with app.test_client() as client:
        with patch("app.fetch_open_food_facts") as mock_fetch:
            mock_fetch.return_value = {
                "product_name": "Nutella",
                "brands": "Nutella, Ferrero",
                "ingredients_text": "Sugar, palm oil, hazelnuts"
            }

            response = client.get("/external-product/3017620422003")

            assert response.status_code == 200

            data = response.get_json()

            assert data["product_name"] == "Nutella"
            assert data["brands"] == "Nutella, Ferrero"
            assert data["code"] == "3017620422003"


def test_external_product_not_found():
    with app.test_client() as client:
        with patch("app.fetch_open_food_facts", return_value=None):
            response = client.get("/external-product/0000000000000")

            assert response.status_code == 404

            data = response.get_json()

            assert data["error"] == "Product not found on Open Food Facts"


def test_import_product():
    original_length = len(inventory)

    with app.test_client() as client:
        with patch("app.fetch_open_food_facts") as mock_fetch:
            mock_fetch.return_value = {
                "product_name": "Nutella",
                "brands": "Nutella, Ferrero",
                "ingredients_text": "Sugar, palm oil, hazelnuts"
            }

            response = client.post(
                "/inventory/import/3017620422003",
                json={
                    "price": 500,
                    "stock": 15
                }
            )

            assert response.status_code == 201

            data = response.get_json()

            assert data["product_name"] == "Nutella"
            assert data["brands"] == "Nutella, Ferrero"
            assert data["barcode"] == "3017620422003"
            assert data["price"] == 500
            assert data["stock"] == 15

            assert len(inventory) == original_length + 1

            inventory.pop()


def test_import_product_missing_price():
    with app.test_client() as client:
        with patch("app.fetch_open_food_facts") as mock_fetch:
            mock_fetch.return_value = {
                "product_name": "Nutella",
                "brands": "Nutella, Ferrero"
            }

            response = client.post(
                "/inventory/import/3017620422003",
                json={
                    "stock": 15
                }
            )

            assert response.status_code == 400

            data = response.get_json()

            assert data["error"] == "Price is required"


def test_import_product_negative_stock():
    with app.test_client() as client:
        with patch("app.fetch_open_food_facts") as mock_fetch:
            mock_fetch.return_value = {
                "product_name": "Nutella",
                "brands": "Nutella, Ferrero"
            }

            response = client.post(
                "/inventory/import/3017620422003",
                json={
                    "price": 500,
                    "stock": -5
                }
            )

            assert response.status_code == 400

            data = response.get_json()

            assert data["error"] == "Stock cannot be negative"