import pytest
from main import app
from httpx import AsyncClient, ASGITransport

transport = ASGITransport(app=app)


@pytest.mark.asyncio
async def test_create_api_product():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.post("/product/create",
                                     headers={
                                         "Content-Type": "application/json"
                                     },
                                     json={
                                         "name": "Title",
                                         "description": "Description",
                                         "price": 28.45,
                                         "amount": 5,
                                         "service": 0
                                     })
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data'] is None
        assert data['error'] is None


@pytest.mark.asyncio
async def test_get_api_product():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.post("/product/product/1")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data']['products'][0]["name"] == "Title"
        assert data['data']['products'][0]["description"] == "Description"
        assert data['data']['products'][0]["price"] == 28.45
        assert data['data']['products'][0]["amount"] == 5
        assert data['error'] is None


@pytest.mark.asyncio
async def test_update_api_product():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.post("/product/update/1",
                                     headers={
                                         "Content-Type": "application/json"
                                     },
                                     json={
                                         "name": "Title2",
                                         "description": "Description2",
                                         "price": 35.45,
                                         "amount": 10,
                                         "service": 0
                                     })
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data'] is None
        assert data['error'] is None


@pytest.mark.asyncio
async def test_gets_api_products():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.get("/product/products")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        print(data)
        for carousel in data['data']['products']:
            assert carousel['id'] in [1, 2]
            assert carousel['name'] in ["Title", "Title2"]
            assert carousel['description'] in ["Description", "Description2"]
            assert carousel['price'] in [35.45, 28.45]
            assert carousel['amount'] in [10, 5]
        assert data['error'] is None


@pytest.mark.asyncio
async def test_delete_api_product():
    async with AsyncClient(
            transport=transport,
            base_url='http://localhost:8000'
    ) as client:
        response = await client.post("/product/delete/1")
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data'] is None
        assert data['error'] is None
