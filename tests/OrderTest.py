import sys

sys.path.append("D:/dev/python/projects/bot_order")

import pytest
from database.Orders import OrderManager
from database.main import async_session_maker


@pytest.mark.asyncio
async def test_create_order():
    async with async_session_maker() as session:
        order_manager = OrderManager(session)
        order = await order_manager.create_order(1, 1)
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
        order_manager = OrderManager(session)
        query = await order_manager.get_order(1)
        assert query.product_id == 1
        assert query.user_id == 1
        assert query.status == True


@pytest.mark.asyncio
async def test_get_orders():
    async with async_session_maker() as session:
        order_manager = OrderManager(session)
        orders = await order_manager.get_orders()
        for order in orders:
            assert order.product_id == 1
            assert order.user_id == 1
            assert order.status == True

@pytest.mark.asyncio
async def test_delete_order():
    async with async_session_maker() as session:
        order_manager = OrderManager(session)
        query = await order_manager.delete_order(1)
        assert query is True
