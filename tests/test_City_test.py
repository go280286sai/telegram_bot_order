import pytest
from database.City import CityManager
from database.main import async_session_maker, City


@pytest.mark.asyncio
async def test_create_city():
    async with async_session_maker() as session:
        city_manager = CityManager(session)
        query = await city_manager.create_city(
            name="City1",
            post_id=1)
        assert isinstance(query, City)
        query = await city_manager.create_city(
            name="City2",
            post_id=2)
        assert isinstance(query, City)


@pytest.mark.asyncio
async def test_get_city():
    async with async_session_maker() as session:
        city_manager = CityManager(session)
        query = await city_manager.get_city(1)
        for city in query:
            assert city.name == "City1"
        query = await city_manager.get_city(2)
        for city in query:
            assert city.name == "City2"


@pytest.mark.asyncio
async def test_update_city():
    async with async_session_maker() as session:
        city_manager = CityManager(session)
        city = await city_manager.update_city(
            idx=1,
            name="City3",
            post_id=2
        )
        assert city is True
        city = await city_manager.update_city(
            idx=2,
            name="City4",
            post_id=1
        )
        assert city is True


@pytest.mark.asyncio
async def test_get_cities():
    async with async_session_maker() as session:
        city_manager = CityManager(session)
        cities = await city_manager.get_cities()
        for city in cities:
            assert city.name in ["City3", "City4"]
            assert city.post_id in [1, 2]


@pytest.mark.asyncio
async def test_delete_city():
    async with async_session_maker() as session:
        city_manager = CityManager(session)
        query = await city_manager.delete_city(1)
        assert query is True
        query = await city_manager.delete_city(2)
        assert query is True
