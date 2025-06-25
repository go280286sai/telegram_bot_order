import sys
import pytest
from database.Deliveries import DeliveryManager
from database.main import async_session_maker

sys.path.append("D:/dev/python/projects/bot_order")
NAME = 'Post'
CITY = 'Kharkiv'
ADDRESS = 'Sumska, 16'


@pytest.mark.asyncio
async def test_create_delivery():
    async with async_session_maker() as session:
        delivery_manager = DeliveryManager(session)
        delivery = await delivery_manager.create_delivery(
            name=NAME,
            city=CITY,
            address=ADDRESS
        )
        assert delivery is True


@pytest.mark.asyncio
async def test_get_delivery():
    async with async_session_maker() as session:
        order_manager = DeliveryManager(session)
        query = await order_manager.get_delivery(1)
        assert query.name == NAME
        assert query.city == CITY
        assert query.address == ADDRESS


@pytest.mark.asyncio
async def test_update_deliveries():
    async with async_session_maker() as session:
        delivery_manager = DeliveryManager(session)
        delivery = await delivery_manager.update_delivery(
            idx=1,
            name=NAME + "1",
            city=CITY + "1",
            address=ADDRESS + "1"
        )
        assert delivery is True


@pytest.mark.asyncio
async def test_get_deliveries():
    async with async_session_maker() as session:
        delivery_manager = DeliveryManager(session)
        deliveries = await delivery_manager.get_deliveries()
        for delivery in deliveries:
            assert delivery.name == NAME + "1"
            assert delivery.city == CITY + "1"
            assert delivery.address == ADDRESS + "1"


@pytest.mark.asyncio
async def test_delete_delivery():
    async with async_session_maker() as session:
        delivery_manager = DeliveryManager(session)
        query = await delivery_manager.delete_delivery(1)
        assert query is True
