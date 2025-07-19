import pytest
from main import app
from httpx import AsyncClient, ASGITransport

transport = ASGITransport(app=app)


@pytest.mark.asyncio
async def test_create_api_review():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.post("/review/create",
                                     headers={
                                         "Content-Type": "application/json"
                                     },
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
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.post("/review/update/1",
                                     headers={
                                         "Content-Type": "application/json"
                                     },
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
        response = await client.post("/review/update/1",
                                     headers={
                                         "Content-Type": "application/json"
                                     },
                                     json={
                                         "name": "Author2",
                                         "text": "Description2",
                                         "gender": 5
                                     })
        assert response.status_code == 400
        data = response.json()
        assert data['success'] is False
        assert data['data'] is None
        assert data['error'] is not None
        response = await client.post("/review/update/0",
                                     headers={
                                         "Content-Type": "application/json"
                                     },
                                     json={
                                         "name": "Author2",
                                         "text": "Description2",
                                         "gender": 0
                                     })
        assert response.status_code == 400
        data = response.json()
        assert data['success'] is False
        assert data['data'] is None
        assert data['error'] is not None


@pytest.mark.asyncio
async def test_get_api_review():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.get("/review/reviews")
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
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.post("/review/delete/1")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data'] is None
        assert data['error'] is None
        response = await client.post("/review/delete/1")
        assert response.status_code == 400
