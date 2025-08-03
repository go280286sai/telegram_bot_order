import pytest
from main import app
from httpx import AsyncClient, ASGITransport
import pytest_asyncio

transport = ASGITransport(app=app)


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
            transport=transport,
            base_url="http://test"
    ) as client:
        yield client


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, monkeypatch):
    def mock_background_task(*args, **kwargs):
        return True

    monkeypatch.setattr(
        "routers.user_router.BackgroundTasks.add_task",
        mock_background_task
    )
    response = await client.post("/user/register",
                                 json={
                                     "username": "User",
                                     "password": "qwertyQWERTY0!",
                                     "email": "admin@admin.ua",
                                     "phone": "+55555555555"
                                 })
    assert response.status_code == 200
    data_user = response.json()
    assert data_user['success'] is True
    assert data_user['data']['user']['is_admin'] == "1"
    assert data_user['error'] is False
    response = await client.post("/user/register",
                                 json={
                                     "username": "User1",
                                     "password": "qwertyQWERTY0!",
                                     "email": "admin1@admin.ua",
                                     "phone": "+555555555551"
                                 })
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['user']['is_admin'] == "0"


@pytest.mark.asyncio
async def test_product_success(client: AsyncClient, monkeypatch):
    # Send login and password
    response_user = await client.post("/user/login",
                                      json={
                                          "username": "User",
                                          "password": "qwertyQWERTY0!"
                                      })
    assert response_user.status_code == 200
    data = response_user.json()
    assert data['success'] is True
    # Create a new product
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
    response = await client.post("/product/create",
                                 headers={
                                     "Content-Type": "application/json"
                                 },
                                 json={
                                     "name": "Title",
                                     "description": "Description",
                                     "price": -28.45,
                                     "amount": 5,
                                     "service": 0
                                 })
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] is not None
    response = await client.post("/product/create",
                                 headers={
                                     "Content-Type": "application/json"
                                 },
                                 json={
                                     "name": "Title",
                                     "description": "Description",
                                     "price": 28.45,
                                     "amount": -5,
                                     "service": 0
                                 })
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] is not None
    # Update product
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
    response = await client.post("/product/update/0",
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
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] is not None
    # Get product
    response = await client.post("/product/product/1")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['products'][0]["name"] == "Title2"
    assert data['data']['products'][0]["description"] == "Description2"
    assert data['data']['products'][0]["price"] == 35.45
    assert data['data']['products'][0]["amount"] == 10
    assert data['error'] is None
    response = await client.post("/product/product/0")
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] is not None
    # Gets product
    response = await client.get("/product/products")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    for carousel in data['data']['products']:
        assert carousel['id'] in [1, 2]
        assert carousel['name'] in ["Title", "Title2"]
        assert carousel['description'] in ["Description", "Description2"]
        assert carousel['price'] in [35.45, 28.45]
        assert carousel['amount'] in [10, 5]
    assert data['error'] is None
    # Delete products
    response = await client.post("/product/delete/1")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None
    response = await client.post("/product/delete/1")
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_product_fail(client: AsyncClient, monkeypatch):
    # Send login and password
    response_user = await client.post("/user/login",
                                      json={
                                          "username": "User1",
                                          "password": "qwertyQWERTY0!"
                                      })
    assert response_user.status_code == 200
    data = response_user.json()
    assert data['success'] is True
    # Create a new product
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
    assert response.status_code == 403
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Permission denied"
    # Update product
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
    assert response.status_code == 403
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Permission denied"
    # Get product
    response = await client.post("/product/product/1")
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == 'No products'
    # Gets product
    response = await client.get("/product/products")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is not None
    assert data['error'] is None
    # Delete products
    response = await client.post("/product/delete/1")
    assert response.status_code == 403
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] == "Permission denied"


@pytest.mark.asyncio
async def test_delete_users(client: AsyncClient, monkeypatch):
    response_user = await client.post("/user/login",
                                      json={
                                          "username": "User",
                                          "password": "qwertyQWERTY0!"
                                      })
    assert response_user.status_code == 200
    data = response_user.json()
    assert data['success'] is True
    response_user = await client.post("/user/delete/2")
    assert response_user.status_code == 200
    response_user = await client.post("/user/delete/1")
    assert response_user.status_code == 200
