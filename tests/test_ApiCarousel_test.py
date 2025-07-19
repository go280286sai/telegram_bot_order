import pytest
from main import app
from httpx import AsyncClient, ASGITransport

transport = ASGITransport(app=app)


@pytest.mark.asyncio
async def test_create_api_carousel():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.post("/front/carousel/create", json={
            "title": "Title",
            "description": "Description",
            "image": "Image"
        })
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data'] is None
        assert data['error'] is None


@pytest.mark.asyncio
async def test_update_api_carousel():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.post("/front/carousel/update/1",
                                     headers={
                                         "Content-Type": "application/json"
                                     },
                                     json={
                                         "title": "Title2",
                                         "description": "Description2",
                                         "image": "Image2"
                                     })
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data'] is None
        assert data['error'] is None
        response = await client.post("/front/carousel/update/0",
                                     headers={
                                         "Content-Type": "application/json"
                                     },
                                     json={
                                         "title": "Title2",
                                         "description": "Description2",
                                         "image": "Image2"
                                     })
        assert response.status_code == 400
        data = response.json()
        assert data['success'] is False
        assert data['data'] is None
        assert data['error'] is not None


@pytest.mark.asyncio
async def test_get_api_carousel():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.get(
            "http://127.0.0.1:8000/front/carousel/gets")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        for carousel in data['data']['carousels']:
            assert carousel['id'] == 1
            assert carousel['title'] == "Title2"
            assert carousel['description'] == "Description2"
            assert carousel['image'] == "Image2"
        assert data['error'] is None


@pytest.mark.asyncio
async def test_delete_api_carousel():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.post("/front/carousel/delete/1")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data'] is None
        assert data['error'] is None
        response = await client.post("/front/carousel/delete/0")
        assert response.status_code == 400
        data = response.json()
        assert data['success'] is False
        assert data['data'] is None
        assert data['error'] is not None
