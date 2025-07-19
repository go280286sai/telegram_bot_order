import json
from datetime import datetime

import pytest

from main import app
from httpx import AsyncClient, ASGITransport
import pytest_asyncio
from types import SimpleNamespace

from routers import OrderRouter, UserRouter

transport = ASGITransport(app=app)


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(
            transport=transport,
            base_url="http://test"
    ) as client:
        yield client


@pytest.mark.asyncio
async def test_order_created():
    async with AsyncClient(
            transport=transport,
            base_url="http://test",
            cookies={
                "user_id": "123",
                "cart": '[{"product_id": 1, "quantity": 2}]',
                "delivery": '{"address": "Main St", "city": "Testville"}'
            }) as client:
        payload = {
            "transaction": "tx_456",
            "cardTotal": 99.99
        }
        response = await client.post("/order/create", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


@pytest.mark.asyncio
async def test_create_order_missing_user():
    async with AsyncClient(
            transport=transport,
            base_url="http://127.0.0.1:8000",
            cookies={
                "user_id": "123",
                "cart": '[{"product_id": 1, "quantity": 2}]',
            }
    ) as client:
        payload = {
            "transaction": "tx_456",
            "cardTotal": 99.99
        }

        response = await client.post("/order/create", json=payload)
        assert response.status_code == 400
        assert "No delivery" in response.text


@pytest.mark.asyncio
async def test_create_order_missing_delivery():
    async with AsyncClient(
            transport=transport,
            base_url="http://127.0.0.1:8000",
            cookies={
                "cart": '[{"product_id": 1, "quantity": 2}]',
                "delivery": '{"address": "Main St", "city": "Testville"}'
            }
    ) as client:
        payload = {
            "transaction": "tx_456",
            "cardTotal": 99.99
        }

        response = await client.post("/order/create", json=payload)
        assert response.status_code == 400
        assert "User does not exist" in response.text


@pytest.mark.asyncio
async def test_get_orders_user():
    async with AsyncClient(
            transport=transport,
            base_url="http://127.0.0.1:8000",
    ) as client:
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
        assert data['data'] is None
        assert data['error'] is None


@pytest.mark.asyncio
async def test_get_orders_user_fail():
    async with AsyncClient(
            transport=transport,
            base_url="http://127.0.0.1:8000",
            cookies={
                "user_id": "0",
            }
    ) as client:
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
        assert data['data']['orders'] == []
        assert data['error'] is None


@pytest.mark.asyncio
async def test_get_orders_pay_fail_card():
    async with AsyncClient(
            transport=transport,
            base_url="http://127.0.0.1:8000",
    ) as client:
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
async def test_get_orders_pay_fail_total():
    async with AsyncClient(
            transport=transport,
            base_url="http://127.0.0.1:8000",
    ) as client:
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
async def test_get_orders_pay_fail_month():
    async with AsyncClient(
            transport=transport,
            base_url="http://127.0.0.1:8000",
    ) as client:
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
async def test_get_orders_pay_fail_year():
    async with AsyncClient(
            transport=transport,
            base_url="http://127.0.0.1:8000",
    ) as client:
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
async def test_get_orders_pay_fail_cvv():
    async with AsyncClient(
            transport=transport,
            base_url="http://127.0.0.1:8000",
    ) as client:
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
async def test_order_gets(monkeypatch):
    async with AsyncClient(
            transport=transport,
            base_url="http://127.0.0.1:8000",
            cookies={
                "user_id": '1'
            }
    ) as client:
        async def mock_is_admin(self, *args, **kwargs):
            return True

        monkeypatch.setattr('routers.OrderRouter.is_admin', mock_is_admin)
        response = await client.post("/order/gets")

        assert response.status_code == 200
        data = response.json()
        assert data['data'] is not None
        assert data['error'] is None


@pytest.mark.asyncio
async def test_get_orders(monkeypatch):
    async with AsyncClient(
            transport=transport,
            base_url="http://127.0.0.1:8000",
            cookies={
                "user_id": '1'
            }
    ) as client:
        async def mock_is_admin(self, *args, **kwargs):
            return True

        monkeypatch.setattr('routers.OrderRouter.is_admin', mock_is_admin)

        async def mock_set_invoice_order(self, *args, **kwargs):
            return True

        monkeypatch.setattr(
            OrderRouter.OrderManager,
            'set_invoice_order',
            mock_set_invoice_order
        )
        user = SimpleNamespace(email="admin@admin.ua")

        async def mock_get_user(self, *args, **kwargs):
            return user

        monkeypatch.setattr(UserRouter.UserManager, 'get_user', mock_get_user)

        async def mock_send_emails(*args, **kwargs):
            return True

        monkeypatch.setattr(OrderRouter, 'send_emails', mock_send_emails)
        payload = {
            "body": "123456789"
        }
        response = await client.post("/order/send_invoice/1/1", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data['data'] is None
        assert data['error'] is None


@pytest.mark.asyncio
async def test_get_orders_fail_user(monkeypatch):
    async with AsyncClient(
            transport=transport,
            base_url="http://127.0.0.1:8000",
            cookies={
                "user_id": '1'
            }
    ) as client:
        async def mock_is_admin(self, *args, **kwargs):
            return True

        monkeypatch.setattr('routers.OrderRouter.is_admin', mock_is_admin)

        async def mock_set_invoice_order(self, *args, **kwargs):
            return False

        monkeypatch.setattr(
            OrderRouter.OrderManager,
            'set_invoice_order',
            mock_set_invoice_order
        )
        user = SimpleNamespace(email="admin@admin.ua")

        async def mock_get_user(self, *args, **kwargs):
            return user

        monkeypatch.setattr(UserRouter.UserManager, 'get_user', mock_get_user)

        async def mock_send_emails(*args, **kwargs):
            return True

        monkeypatch.setattr(OrderRouter, 'send_emails', mock_send_emails)
        payload = {
            "body": "123456789"
        }
        response = await client.post("/order/send_invoice/1/1", json=payload)

        assert response.status_code == 400
        data = response.json()
        assert data['data'] is None
        assert data['error'] is not None


@pytest.mark.asyncio
async def test_add_comment(monkeypatch):
    async with AsyncClient(
            transport=transport,
            base_url="http://127.0.0.1:8000",
            cookies={
                "user_id": '1'
            }
    ) as client:
        async def mock_is_admin(self, *args, **kwargs):
            return True

        monkeypatch.setattr('routers.OrderRouter.is_admin', mock_is_admin)

        async def mock_add_comment(self, *args, **kwargs):
            return True

        monkeypatch.setattr(
            OrderRouter.OrderManager,
            'add_comment',
            mock_add_comment
        )

        payload = {
            "body": "Comment"
        }
        response = await client.post("/order/add_comment/1", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data['data'] is None
        assert data['error'] is None


@pytest.mark.asyncio
async def test_get_predict(monkeypatch):
    async with AsyncClient(
            transport=transport,
            base_url="http://127.0.0.1:8000",
            cookies={
                "user_id": '1'
            }
    ) as client:
        async def mock_is_admin(self, *args, **kwargs):
            return True

        monkeypatch.setattr('routers.OrderRouter.is_admin', mock_is_admin)

        async def mock_get_predict(self, *args, **kwargs):
            return []

        monkeypatch.setattr(
            OrderRouter.OrderManager,
            'get_predict',
            mock_get_predict
        )
        response = await client.post("/order/get_predict/7")

        assert response.status_code == 200
        data = response.json()
        assert data['data'] is not None
        assert data['error'] is None


@pytest.mark.asyncio
async def test_get_view(monkeypatch):
    async with AsyncClient(
            transport=transport,
            base_url="http://127.0.0.1:8000",
            cookies={
                "user_id": '1',
                "delivery": '{"post_id": 1, "city_id": 1, "address": 1}'
            }
    ) as client:
        async def mock_is_admin(self, *args, **kwargs):
            return True

        monkeypatch.setattr('routers.OrderRouter.is_admin', mock_is_admin)

        async def mock_get_predict(self, *args, **kwargs):
            return []

        monkeypatch.setattr(
            OrderRouter.OrderManager,
            'get_predict',
            mock_get_predict
        )

        class User:
            first_name = "User"
            last_name = "Admin"
            phone = "123456789"
            email = "admin@admin.com"

        class Order:
            id = 1
            products = str(json.dumps({'1': 1}))
            user_id = 1
            user = User()
            delivery = str(json.dumps(
                {
                    "post_id": 1,
                    "city_id": 1,
                    "address": 1
                }))
            total = 500.00
            transaction_id = "123"
            invoice = "456"
            created_at = datetime.now()

        order = Order()

        async def mock_get_order(self, *args, **kwargs):
            return order

        monkeypatch.setattr(
            OrderRouter.OrderManager,
            'get_order',
            mock_get_order
        )

        class Products:
            id = 1
            name = "Product"
            description = "This product is a test"
            amount = 10
            price = 10.50

        products = Products()

        async def mock_get_products(self, *args, **kwargs):
            return products

        monkeypatch.setattr(
            OrderRouter.ProductManager,
            'get_product',
            mock_get_products
        )

        class Delivery:
            post_name = "Mist"
            city_name = "San Francisco"
            address_name = "123 San Francisco, CA"

        async def mock_get_delivery(self, *args, **kwargs):
            return {
                "post_name": "Mist",
                "city_name": "San Francisco",
                "address_name": "123 San Francisco, CA",
            }

        monkeypatch.setattr(
            OrderRouter.OrderManager,
            'get_delivery',
            mock_get_delivery
        )
        response = await client.post("/order/get_view/1")

        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data']['id'] == 1
        assert data['data']['total'] == 500.00
        assert data['data']['invoice'] == "456"
        assert data['data']['user']['first_name'] == "User"
        assert data['data']['user']['last_name'] == "Admin"
        assert data['data']['user']['phone'] == "123456789"
        assert data['data']['user']['email'] == "admin@admin.com"
        assert data['data']['delivery']['post_name'] == "Mist"
        assert data['data']['delivery']['city_name'] == "San Francisco"
        assert data["error"] is None


@pytest.mark.asyncio
async def test_delete(monkeypatch):
    async with AsyncClient(
            transport=transport,
            base_url="http://127.0.0.1:8000",
            cookies={
                "user_id": '1'
            }
    ) as client:
        async def mock_is_admin(self, *args, **kwargs):
            return True

        monkeypatch.setattr('routers.OrderRouter.is_admin', mock_is_admin)
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
