import pytest
from database.Orders import OrderManager
from database.Products import ProductManager
from database.User import UserManager
from database.Deliveries import DeliveryManager
from database.main import async_session_maker


@pytest.mark.asyncio
async def test_create_order():
    async with async_session_maker() as session:
        order_manager = OrderManager(session)
        order = await order_manager.create_order(
            products="some product",
            user_id=1,
            delivery_id=1,
            total=500.00,
            transaction_id="123")
        assert order is True


@pytest.mark.asyncio
async def test_set_status():
    async with async_session_maker() as session:
        order_manager = OrderManager(session)
        query = await order_manager.set_status(1, 1)
        assert query is True


@pytest.mark.asyncio
async def test_get_order():
    async with async_session_maker() as session:
        # Product
        product_manager = ProductManager(session)
        await product_manager.create_product(
            name="Product 1",
            description="Product 1",
            amount=1,
            price=500.00
        )
        # User
        user_manager = UserManager(session)
        await user_manager.create_user(
            username="Alex",
            password="0000",
            phone="0123456789",
            email="admin@admin.com"
        )
        # Delivery
        delivery_manager = DeliveryManager(session)
        await delivery_manager.create_delivery(1, 1, 1)

        order_manager = OrderManager(session)
        query = await order_manager.get_order(1)
        assert query.user_id == 1
        assert query.delivery_id == 1
        assert query.total == 500.00
        assert query.user.username == "Alex"
        assert query.user.phone == "0123456789"


@pytest.mark.asyncio
async def test_get_orders():
    async with async_session_maker() as session:
        order_manager = OrderManager(session)
        orders = await order_manager.get_orders()
        for query in orders:
            assert query.user_id == 1
            assert query.delivery_id == 1
            assert query.total == 500.00
            assert query.user.username == "Alex"
            assert query.user.phone == "0123456789"


@pytest.mark.asyncio
async def test_get_order_two():
    async with async_session_maker() as session:
        order_manager = OrderManager(session)
        orders = await order_manager.get_orders_user(1)
        for query in orders:
            assert query['id'] == 1
            assert query['total'] == 500.00


@pytest.mark.asyncio
async def test_delete_order():
    async with async_session_maker() as session:
        order_manager = OrderManager(session)
        query = await order_manager.delete_order(1)
        assert query is True
        product_manager = ProductManager(session)
        await product_manager.delete_product(1)
        user_manager = UserManager(session)
        await user_manager.delete_user(1)
        delivery_manager = DeliveryManager(session)
        await delivery_manager.delete_delivery(1)

