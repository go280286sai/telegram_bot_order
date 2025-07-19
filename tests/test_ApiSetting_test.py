import pytest
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.mark.asyncio
async def test_create_api_setting():
    transport = ASGITransport(app=app)
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        payload = {"name": "Title", "value": "Value"}
        response = await client.post("/setting/create", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data'] is None
        assert data['error'] is None


@pytest.mark.asyncio
async def test_update_api_setting():
    transport = ASGITransport(app=app)
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        payload = {"name": "Title2", "value": "Value2"}
        response = await client.post("/setting/update/1", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data'] is None
        assert data['error'] is None
        response = await client.post("/setting/update/0", json=payload)
        assert response.status_code == 400
        data = response.json()
        assert data['success'] is False
        assert data['data'] is None
        assert data['error'] is not None


@pytest.mark.asyncio
async def test_gets_api_settings():
    transport = ASGITransport(app=app)
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.get("/setting/gets")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        for item in data['data']['settings']:
            assert item['id'] > 0
            assert item['name'] in ["Title", "Title2"]
        assert data['error'] is None


@pytest.mark.asyncio
async def test_delete_api_setting():
    transport = ASGITransport(app=app)
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.get("/setting/gets")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        for item in data['data']['settings']:
            response = await client.post(f"/setting/delete/{item['id']}")
            assert response.status_code == 200
            data = response.json()
            assert data['success'] is True
            assert data['data'] is None
            assert data['error'] is None
        result = await client.post("/setting/delete/1")
        assert result.status_code == 400
