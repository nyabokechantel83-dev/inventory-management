# Inventory Management System

This is a simple inventory management system built with Python and Flask.

The system allows a user to add, view, update and delete products. It also connects to the Open Food Facts API so that product information can be searched using a barcode.

## Features

- Add inventory items
- View all inventory items
- View one inventory item
- Update price and stock
- Delete inventory items
- Search for products using a barcode
- Import product information from Open Food Facts
- Input validation and error handling
- CLI interface
- Unit tests

## Technologies Used

- Python
- Flask
- Requests
- Pytest
- Open Food Facts API

## Project Structure

```text
inventory-management/
├── client/
└── server/
    ├── app.py
    ├── cli.py
    ├── requirements.txt
    ├── README.md
    └── tests/
        ├── test_api.py
        ├── test_cli.py
        └── test_external_api.py
        ## Project Status

This project was built as part of a Flask REST API summative lab.