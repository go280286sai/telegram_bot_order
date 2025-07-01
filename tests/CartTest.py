import pytest
from fastapi.testclient import TestClient
from database.Products import ProductManager
from database.main import async_session_maker
from main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_create_product():
    async with async_session_maker() as session:
        product_manager = ProductManager(session)
        await product_manager.create_product(
            name="Product1",
            description="This product is a test",
            amount=2,
            price=10.50)
        product = await product_manager.create_product(
            name="Product2",
            description="This product is a test",
            amount=2,
            price=10.50)
        assert product.name == "Product2"


@pytest.mark.asyncio
async def test_increase_amount():
    product_id = 1
    client.post(
        f"http://127.0.0.1:8000/cart/increase/{product_id}")
    client.post(
        f"http://127.0.0.1:8000/cart/increase/{product_id}")
    response = client.post(
        f"http://127.0.0.1:8000/cart/increase/{product_id}")
    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "data": {"cart": {str(product_id): 2}},
        "error": None
    }


@pytest.mark.asyncio
async def test_decrease_amount():
    product_id = 1
    response = client.post(
        f"http://127.0.0.1:8000/cart/decrease/{product_id}")
    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "data": {"cart": {str(product_id): 1}},
        "error": None
    }


@pytest.mark.asyncio
async def test_cart_all():
    product_id = 2
    client.post(
        f"http://127.0.0.1:8000/cart/increase/{product_id}")
    response = client.post("http://127.0.0.1:8000/cart")
    assert response.status_code == 200
    data = response.json()
    assert len(data['data']['cart']) == 2


@pytest.mark.asyncio
async def test_remove_cart():
    client.post(
        f"http://127.0.0.1:8000/cart/remove/1")
    client.post(
        f"http://127.0.0.1:8000/cart/remove/2")
    response = client.post("http://127.0.0.1:8000/cart")
    assert response.status_code == 200
    data = response.json()
    assert len(data['data']['cart']) == 0


@pytest.mark.asyncio
async def test_remove_product():
    product_id = [1, 2]
    for idx in product_id:
        async with async_session_maker() as session:
            product_manager = ProductManager(session)
            query = await product_manager.delete_product(idx)
            assert query is True


@pytest.mark.asyncio
async def test_add_delivery():
    response = client.post("http://127.0.0.1:8000/cart/delivery",
                           headers={"Content-Type": "application/json"},
                           json={
                               "post_id": "1",
                               "city_id": "1",
                               "address_id": "1",
                           })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"] is None
    assert data["error"] is None


@pytest.mark.asyncio
async def test_get_delivery():
    response = client.post("http://127.0.0.1:8000/cart/delivery/get")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["post_id"] == 1
    assert data["data"]["city_id"] == 1
    assert data["data"]["address_id"] == 1
    assert data["error"] is None


@pytest.mark.asyncio
async def test_delete_delivery():
    response = client.post("http://127.0.0.1:8000/cart/delivery/delete")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"] is None
    assert data["error"] is None
    response = client.post("http://127.0.0.1:8000/cart/delivery/get")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"] is None
    assert data["error"] is None
