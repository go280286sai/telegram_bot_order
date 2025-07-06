import pytest
from httpx import AsyncClient, ASGITransport
from main import app

transport = ASGITransport(app=app)


@pytest.mark.asyncio
async def test_create_api_delivery():
    async with AsyncClient(
            transport=transport,
            base_url="http://127.0.0.1:8000"
    ) as client:
        response = await client.post("/delivery/create",
                                     headers={
                                         "Content-Type": "application/json"
                                     },
                                     json={
                                         "post_id": 1,
                                         "city_id": 1,
                                         "address_id": 1,
                                     })
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data'] is None
        assert data['error'] is None


@pytest.mark.asyncio
async def test_update_api_delivery():
    async with AsyncClient(
            transport=transport,
            base_url="http://127.0.0.1:8000"
    ) as client:
        response = await client.post("/delivery/update/1",
                                     headers={
                                         "Content-Type": "application/json"
                                     },
                                     json={
                                         "post_id": 1,
                                         "city_id": 1,
                                         "address_id": 1,
                                     })
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data'] is None
        assert data['error'] is None
        response = await client.post("/post/create",
                                     headers={
                                         "Content-Type": "application/json"
                                     },
                                     json={
                                         "name": "Post",
                                     })
        assert response.status_code == 200
        response = await client.post("/city/create",
                                     headers={
                                         "Content-Type": "application/json"
                                     },
                                     json={
                                         "name": "City",
                                     })
        assert response.status_code == 200
        response = await client.post("/address/create",
                                     headers={
                                         "Content-Type": "application/json"
                                     },
                                     json={
                                         "name": "Address",
                                     })
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_api_deliveries():
    async with AsyncClient(
            transport=transport,
            base_url="http://127.0.0.1:8000"
    ) as client:
        response = await client.get("/delivery/gets")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['error'] is None


@pytest.mark.asyncio
async def test_delete_api_delivery():
    async with AsyncClient(
            transport=transport,
            base_url="http://127.0.0.1:8000"
    ) as client:
        response = await client.post("/delivery/delete/1")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data'] is None
        assert data['error'] is None
        responses = await client.get("http://127.0.0.1:8000/address/gets")
        data = responses.json()
        for item in data['data']['addresses']:
            response = await client.post(f"/address/delete/{item['id']}")
            assert response.status_code == 200
            data = response.json()
            assert data['success'] is True
            assert data['data'] is None
            assert data['error'] is None
        response = await client.get("/city/gets")
        assert response.status_code == 200
        data = response.json()
        for item in data['data']['cities']:
            await client.post(f"/city/delete/{item['id']}")
            assert response.status_code == 200
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
