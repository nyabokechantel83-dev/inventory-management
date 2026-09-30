from unittest.mock import patch, Mock

import cli


@patch("cli.requests.get")
def test_view_inventory(mock_get, capsys):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "id": 1,
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "price": 450,
            "stock": 10
        }
    ]

    mock_get.return_value = mock_response

    cli.view_inventory()

    output = capsys.readouterr().out

    assert "Organic Almond Milk" in output
    assert "Silk" in output
    assert "450" in output


@patch("cli.requests.get")
@patch("builtins.input", return_value="1")
def test_view_item(mock_input, mock_get, capsys):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar",
        "price": 450,
        "stock": 10
    }

    mock_get.return_value = mock_response

    cli.view_item()

    output = capsys.readouterr().out

    assert "Organic Almond Milk" in output
    assert "Silk" in output
    assert "450" in output


@patch("cli.requests.post")
@patch("builtins.input")
def test_add_item(mock_input, mock_post, capsys):
    mock_input.side_effect = [
        "Blue Jeans",
        "Levi's",
        "Cotton",
        "1200",
        "15"
    ]

    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "id": 3,
        "product_name": "Blue Jeans"
    }

    mock_post.return_value = mock_response

    cli.add_item()

    output = capsys.readouterr().out

    assert "Item added successfully!" in output
    assert "Blue Jeans" in output


@patch("cli.requests.patch")
@patch("builtins.input")
def test_update_item(mock_input, mock_patch, capsys):
    mock_input.side_effect = [
        "1",
        "500",
        "20"
    ]

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "product_name": "Organic Almond Milk",
        "price": 500,
        "stock": 20
    }

    mock_patch.return_value = mock_response

    cli.update_item()

    output = capsys.readouterr().out

    assert "Item updated successfully!" in output
    assert "500" in output
    assert "20" in output


@patch("cli.requests.delete")
@patch("builtins.input", return_value="2")
def test_delete_item(mock_input, mock_delete, capsys):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_delete.return_value = mock_response

    cli.delete_item()

    output = capsys.readouterr().out

    assert "Item deleted successfully!" in output