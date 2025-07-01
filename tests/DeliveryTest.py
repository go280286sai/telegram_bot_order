import pytest
from database.Deliveries import DeliveryManager
from database.City import CityManager
from database.Address import AddressManager
from database.Post import PostManager
from database.main import async_session_maker


@pytest.mark.asyncio
async def test_create_delivery():
    async with async_session_maker() as session:
        delivery_manager = DeliveryManager(session)
        delivery = await delivery_manager.create_delivery(
            post_id=1,
            city_id=1,
            address_id=1
        )
        assert delivery is True
        post_manager = PostManager(session)
        post = await post_manager.create_post(name="Post")
        assert post is True

        city_manager = CityManager(session)
        city = await city_manager.create_city(name="City")
        assert city is True

        address_manager = AddressManager(session)
        address = await address_manager.create_address(name="Address")
        assert address is True



@pytest.mark.asyncio
async def test_get_delivery():
    async with async_session_maker() as session:
        order_manager = DeliveryManager(session)
        query = await order_manager.get_delivery(1)
        assert query['delivery_id'] == 1
        assert query['post_name'] == "Post"
        assert query['city_name'] == "City"
        assert query['address_name'] == "Address"



@pytest.mark.asyncio
async def test_update_deliveries():
    async with async_session_maker() as session:
        delivery_manager = DeliveryManager(session)
        delivery = await delivery_manager.update_delivery(
            idx=1,
            post_id=1,
            city_id=1,
            address_id=1
        )
        assert delivery is True


@pytest.mark.asyncio
async def test_get_deliveries():
    async with async_session_maker() as session:
        delivery_manager = DeliveryManager(session)
        deliveries = await delivery_manager.get_deliveries()
        for delivery in deliveries:
            assert delivery['delivery_id'] == 1
            assert delivery['post_name'] == "Post"
            assert delivery['city_name'] == "City"
            assert delivery['address_name'] == "Address"


@pytest.mark.asyncio
async def test_delete_delivery():
    async with async_session_maker() as session:
        delivery_manager = DeliveryManager(session)
        query = await delivery_manager.delete_delivery(1)
        assert query is True
        post_manager = PostManager(session)
        post = await post_manager.delete_post(1)
        assert post is True

        city_manager = CityManager(session)
        city = await city_manager.delete_city(1)
        assert city is True

        address_manager = AddressManager(session)
        address = await address_manager.delete_address(1)
        assert address is True
