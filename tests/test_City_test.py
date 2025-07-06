import pytest
from database.City import CityManager
from database.main import async_session_maker, City
import pytest_asyncio


@pytest_asyncio.fixture
async def test_create_city():
    async with async_session_maker() as session:
        city_manager = CityManager(session)
        query = await city_manager.create_city(
            name="City")
        assert isinstance(query, City)
        return query.id


@pytest_asyncio.fixture
async def test_get_city(test_create_city):
    async with async_session_maker() as session:
        idx = test_create_city
        city_manager = CityManager(session)
        query = await city_manager.get_city(int(idx))
        assert query.name == "City"
        return idx


@pytest_asyncio.fixture
async def test_update_city(test_get_city):
    async with async_session_maker() as session:
        idx = test_get_city
        city_manager = CityManager(session)
        city = await city_manager.update_city(
            idx=int(idx),
            name="City1",
        )
        assert city is True
        return idx


@pytest.mark.asyncio
async def test_get_cities():
    async with async_session_maker() as session:
        city_manager = CityManager(session)
        cities = await city_manager.get_cities()
        for city in cities:
            assert city.name == "City1"


@pytest.mark.asyncio
async def test_delete_city(test_update_city):
    async with async_session_maker() as session:
        idx = test_update_city
        city_manager = CityManager(session)
        query = await city_manager.delete_city(int(idx))
        assert query is True
