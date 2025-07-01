import pytest
from fastapi.testclient import TestClient

from database.Post import PostManager
from main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_create_api_delivery():
    response = client.post(f"http://127.0.0.1:8000/delivery/create",
                           headers={"Content-Type": "application/json"},
                           json={
                               "post_id": 1,
                               "city_id": 1,
                               "address_id": 1,
                           })
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None


@pytest.mark.asyncio
async def test_update_api_delivery():
    response = client.post(f"http://127.0.0.1:8000/delivery/update/1",
                           headers={"Content-Type": "application/json"},
                           json={
                               "post_id": 1,
                               "city_id": 1,
                               "address_id": 1,
                           })
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None
    response = client.post(f"http://127.0.0.1:8000/post/create",
                           headers={"Content-Type": "application/json"},
                           json={
                               "name": "Post",
                           })
    assert response.status_code == 200
    response = client.post(f"http://127.0.0.1:8000/city/create",
                           headers={"Content-Type": "application/json"},
                           json={
                               "name": "City",
                           })
    assert response.status_code == 200
    response = client.post(f"http://127.0.0.1:8000/address/create",
                           headers={"Content-Type": "application/json"},
                           json={
                               "name": "Address",
                           })
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_api_deliveries():
    response = client.get(f"http://127.0.0.1:8000/delivery/gets")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    for delivery in data['data']['deliveries']:
        assert delivery['delivery_id'] == 1
        assert delivery['post_name'] == "Post"
        assert delivery['city_name'] == "City"
        assert delivery['address_name'] == "Address"
    assert data['error'] is None

    response = client.post(f"http://127.0.0.1:8000/post/delete/1")
    assert response.status_code == 200
    response = client.post(f"http://127.0.0.1:8000/city/delete/1")
    assert response.status_code == 200
    response = client.post(f"http://127.0.0.1:8000/address/delete/1")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_api_delivery():
    response = client.post(f"http://127.0.0.1:8000/delivery/delete/1")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None
