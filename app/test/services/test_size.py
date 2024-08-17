import pytest

from app.test.utils.functions import get_random_price, get_random_string

def test_create_size_service(client, size_uri, size):
    response = client.post(size_uri, json=size)
    print(response.json)
    assert response.status_code == 201
    created_size = response.json
    pytest.assume(created_size["_id"])
    pytest.assume(created_size["name"] == size["name"])
    pytest.assume(created_size["price"] == size["price"])

def test_update_size_service(client, create_size, size_uri):
    current_size = create_size.json
    _id = current_size['_id']
    update_data = {'name': get_random_string(), 'price': get_random_price(1, 5)}
    response = client.put(f"{size_uri}{_id}", json=update_data)
    pytest.assume(response.status_code == 200)
    updated_size = response.json
    for param, value in update_data.items():
        pytest.assume(updated_size[param] == value)

def test_get_size_by_id_service(client, create_size, size_uri):
    current_size = create_size.json
    response = client.get(f'{size_uri}{current_size["_id"]}')
    pytest.assume(response.status_code == 200)
    returned_size = response.json
    for param, value in current_size.items():
        pytest.assume(returned_size[param] == value)

def test_get_sizes_service(client, create_sizes, size_uri):
    response = client.get(size_uri)
    pytest.assume(response.status_code == 200)
    returned_sizes = {size['_id']: size for size in response.json}
    for size in create_sizes:
        _id = size['_id']
        pytest.assume(_id in returned_sizes)
        pytest.assume(returned_sizes[_id]['name'] == size['name'])
        pytest.assume(returned_sizes[_id]['price'] == size['price'])
