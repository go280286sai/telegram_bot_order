import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_create_api_review():
    response = client.post(f"http://127.0.0.1:8000/review/create",
                           headers={"Content-Type": "application/json"},
                           json={
                               "name": "Author",
                               "text": "Description",
                               "gender": 0
                           })
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None


@pytest.mark.asyncio
async def test_update_api_review():
    response = client.post(f"http://127.0.0.1:8000/review/update/1",
                           headers={"Content-Type": "application/json"},
                           json={
                               "name": "Author2",
                               "text": "Description2",
                               "gender": 1
                           })
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None


@pytest.mark.asyncio
async def test_get_api_review():
    response = client.get(f"http://127.0.0.1:8000/review/reviews")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    for review in data['data']['reviews']:
        assert review['id'] == 1
        assert review['name'] == "Author2"
        assert review['text'] == "Description2"
        assert review['gender'] == 1
    assert data['error'] is None


@pytest.mark.asyncio
async def test_delete_api_review():
    response = client.post(f"http://127.0.0.1:8000/review/delete/1")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None
