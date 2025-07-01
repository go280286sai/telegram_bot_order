import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_create_api_product():
    response = client.post(f"http://127.0.0.1:8000/post/create",
                           headers={"Content-Type": "application/json"},
                           json={
                               "name": "Title",
                           })
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None


@pytest.mark.asyncio
async def test_update_api_product():
    response = client.post(f"http://127.0.0.1:8000/post/update/1",
                           headers={"Content-Type": "application/json"},
                           json={
                               "name": "Title2",
                           })
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None


@pytest.mark.asyncio
async def test_gets_api_products():
    response = client.get(f"http://127.0.0.1:8000/post/gets")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    print(data)
    for carousel in data['data']['posts']:
        assert carousel['id'] == 1
        assert carousel['name'] == "Title2"
    assert data['error'] is None


@pytest.mark.asyncio
async def test_delete_api_product():
    response = client.post(f"http://127.0.0.1:8000/post/delete/1")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None
