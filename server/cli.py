import requests

BASE_URL = "http://127.0.0.1:5000"


def view_inventory():
    response = requests.get(f"{BASE_URL}/inventory")

    if response.status_code == 200:
        items = response.json()

        if not items:
            print("\nNo inventory items found.")
            return

        print("\n========== INVENTORY ==========")

        for item in items:
            print(f"ID: {item['id']}")
            print(f"Product: {item['product_name']}")
            print(f"Brand: {item['brands']}")
            print(f"Price: {item['price']}")
            print(f"Stock: {item['stock']}")
            print("-" * 30)
    else:
        print("\nError:", response.json().get("error", "Could not get inventory"))


def view_item():
    item_id = input("\nEnter item ID: ")

    if not item_id.isdigit():
        print("ID must be a number.")
        return

    response = requests.get(f"{BASE_URL}/inventory/{item_id}")

    if response.status_code == 200:
        item = response.json()

        print("\n========== ITEM ==========")
        print(f"ID: {item['id']}")
        print(f"Product: {item['product_name']}")
        print(f"Brand: {item['brands']}")
        print(f"Ingredients: {item['ingredients_text']}")
        print(f"Price: {item['price']}")
        print(f"Stock: {item['stock']}")
    else:
        print("\nError:", response.json().get("error", "Item not found"))


def add_item():
    print("\n========== ADD ITEM ==========")

    product_name = input("Product name: ")
    brands = input("Brand: ")
    ingredients_text = input("Ingredients: ")
    price = input("Price: ")
    stock = input("Stock: ")

    if not product_name or not brands:
        print("Product name and brand are required.")
        return

    try:
        price = float(price)
        stock = int(stock)
    except ValueError:
        print("Price must be a number and stock must be an integer.")
        return

    data = {
        "product_name": product_name,
        "brands": brands,
        "ingredients_text": ingredients_text,
        "price": price,
        "stock": stock
    }

    response = requests.post(
        f"{BASE_URL}/inventory",
        json=data
    )

    if response.status_code == 201:
        item = response.json()

        print("\nItem added successfully!")
        print(f"ID: {item['id']}")
        print(f"Product: {item['product_name']}")
    else:
        print("\nError:", response.json().get("error", "Could not add item"))


def update_item():
    print("\n========== UPDATE ITEM ==========")

    item_id = input("Enter item ID: ")

    if not item_id.isdigit():
        print("ID must be a number.")
        return

    print("\nLeave a field empty if you don't want to change it.")

    price = input("New price: ")
    stock = input("New stock: ")

    data = {}

    if price:
        try:
            data["price"] = float(price)
        except ValueError:
            print("Price must be a number.")
            return

    if stock:
        try:
            data["stock"] = int(stock)
        except ValueError:
            print("Stock must be an integer.")
            return

    if not data:
        print("No changes were entered.")
        return

    response = requests.patch(
        f"{BASE_URL}/inventory/{item_id}",
        json=data
    )

    if response.status_code == 200:
        item = response.json()

        print("\nItem updated successfully!")
        print(f"Product: {item['product_name']}")
        print(f"Price: {item['price']}")
        print(f"Stock: {item['stock']}")
    else:
        print("\nError:", response.json().get("error", "Could not update item"))


def delete_item():
    print("\n========== DELETE ITEM ==========")

    item_id = input("Enter item ID: ")

    if not item_id.isdigit():
        print("ID must be a number.")
        return

    response = requests.delete(
        f"{BASE_URL}/inventory/{item_id}"
    )

    if response.status_code == 200:
        print("\nItem deleted successfully!")
    else:
        print("\nError:", response.json().get("error", "Could not delete item"))


def find_product():
    print("\n========== FIND PRODUCT ==========")

    barcode = input("Enter barcode: ")

    if not barcode.isdigit():
        print("Barcode must contain numbers only.")
        return

    response = requests.get(
        f"{BASE_URL}/external-product/{barcode}"
    )

    if response.status_code == 200:
        product = response.json()

        print("\n========== PRODUCT FOUND ==========")
        print(f"Product: {product['product_name']}")
        print(f"Brand: {product['brands']}")
        print(f"Ingredients: {product['ingredients_text']}")
        print(f"Barcode: {product['code']}")
    else:
        print("\nError:", response.json().get("error", "Product not found"))


def import_product():
    print("\n========== IMPORT PRODUCT ==========")

    barcode = input("Enter barcode: ")

    if not barcode.isdigit():
        print("Barcode must contain numbers only.")
        return

    price = input("Enter selling price: ")
    stock = input("Enter stock: ")

    try:
        price = float(price)
        stock = int(stock)
    except ValueError:
        print("Price must be a number and stock must be an integer.")
        return

    data = {
        "price": price,
        "stock": stock
    }

    response = requests.post(
        f"{BASE_URL}/inventory/import/{barcode}",
        json=data
    )

    if response.status_code == 201:
        item = response.json()

        print("\nProduct imported successfully!")
        print(f"ID: {item['id']}")
        print(f"Product: {item['product_name']}")
        print(f"Brand: {item['brands']}")
        print(f"Price: {item['price']}")
        print(f"Stock: {item['stock']}")
    else:
        print("\nError:", response.json().get("error", "Could not import product"))


def main():
    while True:
        print("\n")
        print("================================")
        print("   INVENTORY MANAGEMENT SYSTEM")
        print("================================")
        print("1. View all inventory")
        print("2. View one item")
        print("3. Add inventory item")
        print("4. Update price/stock")
        print("5. Delete item")
        print("6. Find product by barcode")
        print("7. Import product from Open Food Facts")
        print("8. Exit")
        print("================================")

        choice = input("Choose an option: ")

        if choice == "1":
            view_inventory()

        elif choice == "2":
            view_item()

        elif choice == "3":
            add_item()

        elif choice == "4":
            update_item()

        elif choice == "5":
            delete_item()

        elif choice == "6":
            find_product()

        elif choice == "7":
            import_product()

        elif choice == "8":
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid choice. Please choose 1-8.")


if __name__ == "__main__":
    main()