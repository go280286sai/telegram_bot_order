import pytest

from database.Products import ProductManager
from database.main import async_session_maker
from main import app
from httpx import AsyncClient, ASGITransport
import pytest_asyncio

from routers import order_router

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
async def test_order_created(client: AsyncClient, monkeypatch):
    response_user = await client.post("/user/login",
                                      json={
                                          "username": "User",
                                          "password": "qwertyQWERTY0!"
                                      })
    assert response_user.status_code == 200
    payload = {
        "transaction": "tx_456",
        "cardTotal": 99.99
    }
    await client.post(
        "/cart/increase/1")
    response = await client.post("/cart/delivery/create", json={
        "post_id": 1,
        "city_id": 1,
        "address_id": 1
    })
    assert response.status_code == 200
    response = await client.post("/order/create", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    response = await client.post("/order/get_orders_user",
                                 headers={
                                     "Content-Type": "application/json"
                                 },
                                 json={
                                     "title": "Title",
                                     "description": "Description",
                                     "image": "Image"
                                 })
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is not None
    assert data['error'] is None
    response = await client.post("/order/gets")
    assert response.status_code == 200
    data = response.json()
    assert data['data'] is not None
    assert data['error'] is None

    async def mock_is_admin(self, *args, **kwargs):
        return True

    monkeypatch.setattr('routers.order_router.Middleware.is_admin', mock_is_admin)

    async def mock_set_invoice_order(self, *args, **kwargs):
        return True

    monkeypatch.setattr(
        order_router.Orders.OrderManager,
        'set_invoice_order',
        mock_set_invoice_order
    )
    payload = {
        "body": "123456789"
    }
    response = await client.post("/order/send_invoice/1/1", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data['data'] is None
    assert data['error'] is None
    payload = {
        "body": "Comment"
    }
    response = await client.post("/order/add_comment/1", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data['data'] is None
    assert data['error'] is None
    response = await client.post("/order/get_predict/7")
    assert response.status_code == 400
    data = response.json()
    assert data['data'] is None
    assert data['error'] is not None
    response = await client.post("/order/get_view/1")

    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['id'] == 1
    assert data['data']['total'] == 99.99
    assert data['data']['invoice'] is None
    assert data['data']['user']['first_name'] is None
    assert data['data']['user']['last_name'] is None
    assert data['data']['user']['phone'] == "+55555555555"
    assert data['data']['user']['email'] == "admin@admin.ua"
    assert data['data']['delivery']['post_name'] == "Post"
    assert data['data']['delivery']['city_name'] == "Title"
    assert data["error"] is None
    response = await client.post("/order/delete/1")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'] is None
    assert data['error'] is None
    response = await client.post("/order/delete/1")
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] is not None


@pytest.mark.asyncio
async def test_get_orders_pay_fail_card(client: AsyncClient):
    payload = {
        "cardTotal": 1000.00,
        "cardNumber": "123494561237",
        "cardMonth": "02",
        "cardYear": "26",
        "cardKey": "123"
    }
    response = await client.post("/order/pay",
                                 headers={
                                     "Content-Type": "application/json"
                                 },
                                 json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] in "Invalid card number"


@pytest.mark.asyncio
async def test_get_orders_pay_fail_total(client: AsyncClient):
    payload = {
        "cardTotal": 0,
        "cardNumber": "123494561237",
        "cardMonth": "02",
        "cardYear": "26",
        "cardKey": "123"
    }
    response = await client.post("/order/pay",
                                 headers={
                                     "Content-Type": "application/json"
                                 },
                                 json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] in "Total is zero"


@pytest.mark.asyncio
async def test_get_orders_pay_fail_month(client: AsyncClient):
    payload = {
        "cardTotal": 1000.00,
        "cardNumber": "1234567897894561",
        "cardMonth": "20",
        "cardYear": "26",
        "cardKey": "123"
    }
    response = await client.post("/order/pay",
                                 headers={
                                     "Content-Type": "application/json"
                                 },
                                 json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] in "Invalid expiry month"


@pytest.mark.asyncio
async def test_get_orders_pay_fail_year(client: AsyncClient):
    payload = {
        "cardTotal": 1000.00,
        "cardNumber": "1234567897894561",
        "cardMonth": "08",
        "cardYear": "06",
        "cardKey": "123"
    }
    response = await client.post("/order/pay",
                                 headers={
                                     "Content-Type": "application/json"
                                 },
                                 json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] in "Invalid data year"


@pytest.mark.asyncio
async def test_get_orders_pay_fail_cvv(client: AsyncClient):
    payload = {
        "cardTotal": 1000.00,
        "cardNumber": "1234567897894561",
        "cardMonth": "08",
        "cardYear": "26",
        "cardKey": "13"
    }
    response = await client.post("/order/pay",
                                 headers={
                                     "Content-Type": "application/json"
                                 },
                                 json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
    assert data['data'] is None
    assert data['error'] in "Invalid CVV"


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
