import pytest
from database.Deliveries import DeliveryManager
from database.City import CityManager
from database.Address import AddressManager
from database.Post import PostManager
from database.main import async_session_maker, Delivery, Post, City, Address
import pytest_asyncio


@pytest_asyncio.fixture
async def test_create_delivery():
    async with async_session_maker() as session:
        delivery_manager = DeliveryManager(session)
        delivery = await delivery_manager.create_delivery(
            post_id=1,
            city_id=1,
            address_id=1
        )
        assert isinstance(delivery, Delivery)

        post_manager = PostManager(session)
        post = await post_manager.create_post(name="Post")
        assert isinstance(post, Post)

        city_manager = CityManager(session)
        city = await city_manager.create_city(name="City")
        assert isinstance(city, City)

        address_manager = AddressManager(session)
        address = await address_manager.create_address(name="Address")
        assert isinstance(address, Address)
        return delivery.id


@pytest_asyncio.fixture
async def test_get_delivery(test_create_delivery):
    async with async_session_maker() as session:
        idx = test_create_delivery
        order_manager = DeliveryManager(session)
        query = await order_manager.get_delivery(int(idx))
        assert query['post_name'] == "Post"
        assert query['city_name'] == "City"
        assert query['address_name'] == "Address"
        return idx


@pytest_asyncio.fixture
async def test_update_deliveries(test_get_delivery):
    async with async_session_maker() as session:
        idx = test_get_delivery
        delivery_manager = DeliveryManager(session)
        delivery = await delivery_manager.update_delivery(
            idx=int(idx),
            post_id=1,
            city_id=1,
            address_id=1
        )
        assert delivery is True
        return idx


@pytest_asyncio.fixture
async def test_get_deliveries(test_update_deliveries):
    async with async_session_maker() as session:
        idx = test_update_deliveries
        delivery_manager = DeliveryManager(session)
        deliveries = await delivery_manager.get_deliveries()
        for delivery in deliveries:
            assert delivery['delivery_id'] == int(idx)
            assert delivery['post_name'] == "Post"
            assert delivery['city_name'] == "City"
            assert delivery['address_name'] == "Address"
        return idx


@pytest.mark.asyncio
async def test_delete_delivery(test_get_deliveries):
    async with async_session_maker() as session:
        idx = test_get_deliveries
        delivery_manager = DeliveryManager(session)
        query = await delivery_manager.delete_delivery(int(idx))
        assert query is True
        post_manager = PostManager(session)
        posts = await post_manager.get_posts()
        posts_ = [
            {
                "id": p.id,
                "name": p.name,
            } for p in posts
        ]
        for post in posts_:
            await post_manager.delete_post(post['id'])

        city_manager = CityManager(session)
        cities = await city_manager.get_cities()
        cities_ = [
            {
                "id": p.id,
                "name": p.name,
            } for p in cities
        ]
        for city in cities_:
            await city_manager.delete_city(city['id'])

        address_manager = AddressManager(session)
        address = await address_manager.get_addresses()
        address_ = [
            {
                "id": p.id,
                "name": p.name,
            } for p in address
        ]
        for address in address_:
            await address_manager.delete_address(address['id'])
