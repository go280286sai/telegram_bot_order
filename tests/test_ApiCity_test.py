import pytest
from main import app
from httpx import AsyncClient, ASGITransport

transport = ASGITransport(app=app)


@pytest.mark.asyncio
async def test_create_api_city():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.post("/city/create",
                                     json={
                                         "name": "Title",
                                         "post_id": 1
                                     })
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data'] is None
        assert data['error'] is None
        response = await client.post("/city/create",
                                     json={
                                         "name": "Title",
                                         "post_id": 0
                                     })
        assert response.status_code == 400
        data = response.json()
        assert data['success'] is False
        assert data['data'] is None
        assert data['error'] is not None
        response = await client.post("/post/create",
                                     json={
                                         "name": "Title"
                                     })
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_api_city():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.post("/city/update/1",
                                     json={
                                         "name": "Title2",
                                         "post_id": 2
                                     })
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data'] is None
        assert data['error'] is None
        response = await client.post("/city/update/1",
                                     json={
                                         "name": "Title2",
                                         "post_id": 0
                                     })
        assert response.status_code == 400
        data = response.json()
        assert data['success'] is False
        assert data['data'] is None
        assert data['error'] is not None


@pytest.mark.asyncio
async def test_gets_api_cities():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.get("/city/gets")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        for item in data['data']['cities']:
            assert item['id'] is not None
            assert item['name'] is not None
        assert data['error'] is None


@pytest.mark.asyncio
async def test_get_api_city():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.get("/city/get/1")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        for item in data['data']['cities']:
            assert item['id'] == 1
            assert item['name'] == "Title"
        assert data['error'] is None

        response = await client.get("/city/get/0")
        assert response.status_code == 400
        data = response.json()
        assert data['success'] is False
        assert data['data'] is None
        assert data['error'] is not None


@pytest.mark.asyncio
async def test_delete_api_product():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.get("/city/gets")
        assert response.status_code == 200
        data = response.json()
        for item in data['data']['cities']:
            await client.post(f"/city/delete/{item['id']}")
            assert response.status_code == 200
        response = await client.post("/city/delete/1")
        assert response.status_code == 400
