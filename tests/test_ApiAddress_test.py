import pytest
from httpx import AsyncClient, ASGITransport
from main import app

transport = ASGITransport(app=app)


@pytest.mark.asyncio
async def test_create_api_address():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.post("/address/create", json={"name": "test"})
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data'] is None
        assert data['error'] is None


@pytest.mark.asyncio
async def test_update_api_address():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.post("/address/update/1",
                                     json={
                                         "name": "Title2"
                                     })
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data'] is None
        assert data['error'] is None


@pytest.mark.asyncio
async def test_gets_api_addresses():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.get("http://127.0.0.1:8000/address/gets")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        for item in data['data']['addresses']:
            assert item['id'] == 1
            assert item['name'] == "Title2"
        assert data['error'] is None


@pytest.mark.asyncio
async def test_delete_api_address():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        responses = await client.get("http://127.0.0.1:8000/address/gets")
        data = responses.json()
        for item in data['data']['addresses']:
            response = await client.post(f"/address/delete/{item['id']}")
            assert response.status_code == 200
            data = response.json()
            assert data['success'] is True
            assert data['data'] is None
            assert data['error'] is None
