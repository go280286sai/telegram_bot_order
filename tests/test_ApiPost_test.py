import pytest
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.mark.asyncio
async def test_create_api_post():
    transport = ASGITransport(app=app)
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        payload = {"name": "Title"}
        response = await client.post("/post/create", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data'] is None
        assert data['error'] is None


@pytest.mark.asyncio
async def test_update_api_post():
    transport = ASGITransport(app=app)
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        payload = {"name": "Title2"}
        response = await client.post("/post/update/1", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data'] is None
        assert data['error'] is None


@pytest.mark.asyncio
async def test_gets_api_posts():
    transport = ASGITransport(app=app)
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.get("/post/gets")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        for item in data['data']['posts']:
            assert item['id'] in [1, 2]
            assert item['name'] in ["Title", "Title2"]
        assert data['error'] is None


@pytest.mark.asyncio
async def test_delete_api_post():
    transport = ASGITransport(app=app)
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.get("/post/gets")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        for item in data['data']['posts']:
            response = await client.post(f"/post/delete/{item['id']}")
            assert response.status_code == 200
            data = response.json()
            assert data['success'] is True
            assert data['data'] is None
            assert data['error'] is None
