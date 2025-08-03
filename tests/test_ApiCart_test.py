import pytest
from database.Products import ProductManager
from database.main import async_session_maker
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
async def test_create_product():
    async with async_session_maker() as session:
        product_manager = ProductManager(session)
        await product_manager.create_product(
            name="Product1",
            description="This product is a test",
            amount=3,
            price=10.50)
        product = await product_manager.create_product(
            name="Product2",
            description="This product is a test",
            amount=3,
            price=10.50)
        assert product.name == "Product2"


@pytest.mark.asyncio
async def test_create_delivery(client: AsyncClient):
    response_user = await client.post("/user/login",
                                      json={
                                          "username": "User",
                                          "password": "qwertyQWERTY0!"
                                      })
    assert response_user.status_code == 200
    data = response_user.json()
    assert data['success'] is True
    response = await client.post("/post/create",
                                 json={
                                     "name": "Post"
                                 })
    assert response.status_code == 200
    response = await client.post("/city/create",
                                 json={
                                     "name": "Title",
                                     "post_id": 1
                                 })
    assert response.status_code == 200
    response = await client.post("/address/create",
                                 json={
                                     "name": "test",
                                     "city_id": 1
                                 })
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_increase_amount(client: AsyncClient):
    response_user = await client.post("/user/login",
                                      json={
                                          "username": "User",
                                          "password": "qwertyQWERTY0!"
                                      })
    assert response_user.status_code == 200
    data = response_user.json()
    assert data['success'] is True
    await client.post(
        "/cart/increase/1")
    await client.post(
        "/cart/increase/2")
    await client.post(
        "/cart/increase/1")
    response = await client.post(
        "/cart/increase/1")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data['data']['cart'] is not None
    assert data['error'] is None
    response = await client.post(
        "/cart/decrease/1")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data['data']['cart'] is not None
    assert data["error"] is None
    response = await client.post("/cart/delivery/create", json={
        "post_id": 1,
        "city_id": 1,
        "address_id": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"] is None
    assert data["error"] is None
    response = await client.post("/cart/remove/2")
    assert response.status_code == 200
    response = await client.post("/cart/total_bonus",
                                 json={
                                     "total": 8000,
                                     "bonus": 100
                                 })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"] is None
    assert data["error"] is None
    response = await client.post("/cart/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"] is not None
    assert data["error"] is None
    response = await client.post("/cart/delivery/delete")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["error"] is None
    response = await client.post("/cart/delivery/get")
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert data["error"] == "Delivery is not selected"


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
    response = await client.post("/setting/truncates")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None
