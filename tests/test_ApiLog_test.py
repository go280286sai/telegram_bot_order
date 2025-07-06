import pytest
from main import app
from httpx import AsyncClient, ASGITransport

transport = ASGITransport(app=app)


@pytest.mark.asyncio
async def test_create_api_carousel():
    async with AsyncClient(
            transport=transport,
            base_url="http://127.0.0.1:8000"
    ) as client:
        response = await client.post("/logs/create",
                                     headers={
                                         "Content-Type": "application/json"
                                     },
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
