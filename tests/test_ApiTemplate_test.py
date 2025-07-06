import pytest
from main import app
from httpx import AsyncClient, ASGITransport

transport = ASGITransport(app=app)


@pytest.mark.asyncio
async def test_create_api_template():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.post("/template/create",
                                     headers={
                                         "Content-Type": "application/json"
                                     },
                                     json={
                                         "header": "Header",
                                         "title": "Title",
                                         "body": "Body"
                                     })
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data'] is None
        assert data['error'] is None


@pytest.mark.asyncio
async def test_get_api_template():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.post("/template/get/1")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data']['templates'][0]["header"] == "Header"
        assert data['data']['templates'][0]["title"] == "Title"
        assert data['data']['templates'][0]["body"] == "Body"
        assert data['error'] is None


@pytest.mark.asyncio
async def test_update_api_template():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.post("/template/update/1",
                                     headers={
                                         "Content-Type": "application/json"
                                     },
                                     json={
                                         "header": "Header2",
                                         "title": "Title2",
                                         "body": "Body2"
                                     })
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data'] is None
        assert data['error'] is None


@pytest.mark.asyncio
async def test_gets_api_templates():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.get("/template/gets")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        for item in data['data']['templates']:
            assert item["header"] == "Header2"
            assert item["title"] == "Title2"
            assert item["body"] == "Body2"
        assert data['error'] is None


@pytest.mark.asyncio
async def test_delete_api_template():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.get("/template/gets")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        for item in data['data']['templates']:
            response = await client.post(f"/template/delete/{item['id']}",)
            assert response.status_code == 200
            data = response.json()
            assert data['success'] is True
            assert data['data'] is None
            assert data['error'] is None
