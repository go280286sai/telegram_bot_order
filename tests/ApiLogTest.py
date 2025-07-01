import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_create_api_carousel():
    response = client.post(f"http://127.0.0.1:8000/logs/create",
                           headers={"Content-Type": "application/json"},
                           json={
                               "level": "Test",
                               "name": "Test",
                               "message": "Test"
                           })
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None

