import pytest
from database.City import CityManager
from database.main import async_session_maker


@pytest.mark.asyncio
async def test_create_city():
    async with async_session_maker() as session:
        city_manager = CityManager(session)
        delivery = await city_manager.create_city(
            name="City")
        assert delivery is True


@pytest.mark.asyncio
async def test_get_city():
    async with async_session_maker() as session:
        city_manager = CityManager(session)
        query = await city_manager.get_city(1)
        assert query.name == "City"


@pytest.mark.asyncio
async def test_update_city():
    async with async_session_maker() as session:
        city_manager = CityManager(session)
        city = await city_manager.update_city(
            idx=1,
            name="City" + "1",
        )
        assert city is True


@pytest.mark.asyncio
async def test_get_cities():
    async with async_session_maker() as session:
        city_manager = CityManager(session)
        cities = await city_manager.get_cities()
        for city in cities:
            assert city.name == "City" + "1"


@pytest.mark.asyncio
async def test_delete_city():
    async with async_session_maker() as session:
        city_manager = CityManager(session)
        query = await city_manager.delete_city(1)
        assert query is True
