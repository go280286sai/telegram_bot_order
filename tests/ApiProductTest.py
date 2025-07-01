import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_create_api_product():
    response = client.post(f"http://127.0.0.1:8000/product/create",
                           headers={"Content-Type": "application/json"},
                           json={
                               "name": "Title",
                               "description": "Description",
                               "price": 28.45,
                               "amount": 5
                           })
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None

@pytest.mark.asyncio
async def test_get_api_product():
    response = client.post(f"http://127.0.0.1:8000/product/product/1")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['products'][0]["name"] == "Title"
    assert data['data']['products'][0]["description"] == "Description"
    assert data['data']['products'][0]["price"] == 28.45
    assert data['data']['products'][0]["amount"] == 5
    assert data['error'] is None

@pytest.mark.asyncio
async def test_update_api_product():
    response = client.post(f"http://127.0.0.1:8000/product/update/1",
                           headers={"Content-Type": "application/json"},
                           json={
                               "name": "Title2",
                               "description": "Description2",
                               "price": 35.45,
                               "amount": 10
                           })
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None


@pytest.mark.asyncio
async def test_gets_api_products():
    response = client.get(f"http://127.0.0.1:8000/product/products")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    print(data)
    for carousel in data['data']['products']:
        assert carousel['id'] == 1
        assert carousel['name'] == "Title2"
        assert carousel['description'] == "Description2"
        assert carousel['price'] == 35.45
        assert carousel['amount'] == 10
    assert data['error'] is None


@pytest.mark.asyncio
async def test_delete_api_product():
    response = client.post(f"http://127.0.0.1:8000/product/delete/1")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None
