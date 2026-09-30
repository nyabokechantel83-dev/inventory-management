from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar",
        "price": 450,
        "stock": 10
    },
    {
        "id": 2,
        "product_name": "Chocolate Bar",
        "brands": "Cadbury",
        "ingredients_text": "Sugar, cocoa, milk",
        "price": 150,
        "stock": 20
    }
]


@app.route("/")
def home():
    return jsonify({
        "message": "Inventory Management API is running"
    })


@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory), 200


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = next(
        (item for item in inventory if item["id"] == item_id),
        None
    )

    if not item:
        return jsonify({
            "error": "Inventory item not found"
        }), 404

    return jsonify(item), 200


@app.route("/inventory", methods=["POST"])
def create_item():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    product_name = data.get("product_name")
    brands = data.get("brands")
    ingredients_text = data.get("ingredients_text", "")
    price = data.get("price")
    stock = data.get("stock")

    if not product_name:
        return jsonify({
            "error": "Product name is required"
        }), 400

    if not isinstance(product_name, str):
        return jsonify({
            "error": "Product name must be a string"
        }), 400

    if not brands:
        return jsonify({
            "error": "Brand is required"
        }), 400

    if not isinstance(brands, str):
        return jsonify({
            "error": "Brand must be a string"
        }), 400

    if price is None:
        return jsonify({
            "error": "Price is required"
        }), 400

    if not isinstance(price, (int, float)):
        return jsonify({
            "error": "Price must be a number"
        }), 400

    if price < 0:
        return jsonify({
            "error": "Price cannot be negative"
        }), 400

    if stock is None:
        return jsonify({
            "error": "Stock is required"
        }), 400

    if not isinstance(stock, int):
        return jsonify({
            "error": "Stock must be an integer"
        }), 400

    if stock < 0:
        return jsonify({
            "error": "Stock cannot be negative"
        }), 400

    new_id = max(
        [item["id"] for item in inventory],
        default=0
    ) + 1

    new_item = {
        "id": new_id,
        "product_name": product_name,
        "brands": brands,
        "ingredients_text": ingredients_text,
        "price": price,
        "stock": stock
    }

    inventory.append(new_item)

    return jsonify(new_item), 201


@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    item = next(
        (item for item in inventory if item["id"] == item_id),
        None
    )

    if not item:
        return jsonify({
            "error": "Inventory item not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    if "product_name" in data:
        if not isinstance(data["product_name"], str) or not data["product_name"].strip():
            return jsonify({
                "error": "Product name must be a non-empty string"
            }), 400

        item["product_name"] = data["product_name"]

    if "brands" in data:
        if not isinstance(data["brands"], str) or not data["brands"].strip():
            return jsonify({
                "error": "Brand must be a non-empty string"
            }), 400

        item["brands"] = data["brands"]

    if "ingredients_text" in data:
        if not isinstance(data["ingredients_text"], str):
            return jsonify({
                "error": "Ingredients must be a string"
            }), 400

        item["ingredients_text"] = data["ingredients_text"]

    if "price" in data:
        if not isinstance(data["price"], (int, float)):
            return jsonify({
                "error": "Price must be a number"
            }), 400

        if data["price"] < 0:
            return jsonify({
                "error": "Price cannot be negative"
            }), 400

        item["price"] = data["price"]

    if "stock" in data:
        if not isinstance(data["stock"], int):
            return jsonify({
                "error": "Stock must be an integer"
            }), 400

        if data["stock"] < 0:
            return jsonify({
                "error": "Stock cannot be negative"
            }), 400

        item["stock"] = data["stock"]

    return jsonify(item), 200


@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = next(
        (item for item in inventory if item["id"] == item_id),
        None
    )

    if not item:
        return jsonify({
            "error": "Inventory item not found"
        }), 404

    inventory.remove(item)

    return jsonify({
        "message": "Inventory item deleted successfully"
    }), 200


def fetch_open_food_facts(barcode):
    url = f"https://world.openfoodfacts.org/api/v3/product/{barcode}.json"

    headers = {
        "User-Agent": "InventoryManagementSystem/1.0 (test@example.com)"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    product = data.get("product")

    if not product:
        return None

    return product


@app.route("/external-product/<barcode>", methods=["GET"])
def get_external_product(barcode):
    try:
        product = fetch_open_food_facts(barcode)

        if not product:
            return jsonify({
                "error": "Product not found on Open Food Facts"
            }), 404

        return jsonify({
            "product_name": product.get("product_name", ""),
            "brands": product.get("brands", ""),
            "ingredients_text": product.get("ingredients_text", ""),
            "code": barcode
        }), 200

    except requests.RequestException:
        return jsonify({
            "error": "Could not connect to Open Food Facts"
        }), 503


@app.route("/inventory/import/<barcode>", methods=["POST"])
def import_product(barcode):
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Request body is required"
            }), 400

        price = data.get("price")
        stock = data.get("stock")

        if price is None:
            return jsonify({
                "error": "Price is required"
            }), 400

        if not isinstance(price, (int, float)):
            return jsonify({
                "error": "Price must be a number"
            }), 400

        if price < 0:
            return jsonify({
                "error": "Price cannot be negative"
            }), 400

        if stock is None:
            return jsonify({
                "error": "Stock is required"
            }), 400

        if not isinstance(stock, int):
            return jsonify({
                "error": "Stock must be an integer"
            }), 400

        if stock < 0:
            return jsonify({
                "error": "Stock cannot be negative"
            }), 400

        product = fetch_open_food_facts(barcode)

        if not product:
            return jsonify({
                "error": "Product not found on Open Food Facts"
            }), 404

        new_id = max(
            [item["id"] for item in inventory],
            default=0
        ) + 1

        new_item = {
            "id": new_id,
            "product_name": product.get("product_name", ""),
            "brands": product.get("brands", ""),
            "ingredients_text": product.get("ingredients_text", ""),
            "barcode": barcode,
            "price": price,
            "stock": stock
        }

        inventory.append(new_item)

        return jsonify(new_item), 201

    except requests.RequestException:
        return jsonify({
            "error": "Could not connect to Open Food Facts"
        }), 503


if __name__ == "__main__":
    app.run(debug=True)