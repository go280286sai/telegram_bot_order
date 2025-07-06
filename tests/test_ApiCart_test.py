import pytest
from database.Products import ProductManager
from database.main import async_session_maker
from main import app
from httpx import AsyncClient, ASGITransport

transport = ASGITransport(app=app)


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
    async with AsyncClient(
            transport=transport,
            base_url="http://localhost:8000"
    ) as client:
        product_id = 1
        await client.post(
            f"/cart/increase/{product_id}")
        await client.post(
            f"/cart/increase/{product_id}")
        response = await client.post(
            f"/cart/increase/{product_id}")
        assert response.status_code == 200
        assert response.json() == {
            "success": True,
            "data": {"cart": {str(product_id): 2}},
            "error": None
        }


@pytest.mark.asyncio
async def test_decrease_amount():
    async with AsyncClient(
            transport=transport,
            base_url="http://localhost:8000"
    ) as client:
        product_id = 1
        response = await client.post(
            f"/cart/decrease/{product_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["error"] is None


@pytest.mark.asyncio
async def test_cart_all():
    async with AsyncClient(
            transport=transport,
            base_url="http://localhost:8000"
    ) as client:
        product_id = 2
        response = await client.post(f"/cart/increase/{product_id}")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_remove_cart():
    async with AsyncClient(
            transport=transport,
            base_url="http://localhost:8000"
    ) as client:
        await client.post("/cart/remove/1")
        response = await client.post("/cart/remove/2")
        assert response.status_code == 200


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
    async with AsyncClient(
            transport=transport,
            base_url="http://localhost:8000"
    ) as client:
        response = await client.post("/cart/delivery/create/1")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"] is None
        assert data["error"] is None


@pytest.mark.asyncio
async def test_get_delivery():
    async with AsyncClient(
            transport=transport,
            base_url="http://localhost:8000"
    ) as client:
        response = await client.post("/cart/delivery/get")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert data["error"] == "Delivery is not selected"


@pytest.mark.asyncio
async def test_delete_delivery_cookie():
    async with AsyncClient(
            transport=transport,
            base_url="http://localhost:8000"
    ) as client:
        client.cookies.set("delivery", "mock_value")
        response = await client.post("cart/delivery/delete")
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] is True
        assert response_data["data"] is None
        assert response_data["error"] is None

        assert "delivery" not in response.cookies
