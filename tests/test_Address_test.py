import pytest
from database.Address import AddressManager
from database.main import async_session_maker, Address
import pytest_asyncio


@pytest_asyncio.fixture
async def test_create_address():
    async with async_session_maker() as session:
        address_manager = AddressManager(session)
        address = await address_manager.create_address(
            name="Address")
        assert isinstance(address, Address)
        return address.id


@pytest_asyncio.fixture
async def test_get_address(test_create_address):
    async with async_session_maker() as session:
        idx = test_create_address
        address_manager = AddressManager(session)
        query = await address_manager.get_address(int(idx))
        assert query.name == "Address"
        return idx


@pytest_asyncio.fixture
async def test_update_address(test_get_address):
    async with async_session_maker() as session:
        idx = test_get_address
        address_manager = AddressManager(session)
        address = await address_manager.update_address(
            idx=int(idx),
            name="Address1",
        )
        assert address is True
        return idx


@pytest.mark.asyncio
async def test_get_addresses():
    async with async_session_maker() as session:
        address_manager = AddressManager(session)
        addresses = await address_manager.get_addresses()
        for address in addresses:
            assert address.name == "Address1"


@pytest.mark.asyncio
async def test_delete_address(test_get_address):
    async with async_session_maker() as session:
        idx = test_get_address
        address_manager = AddressManager(session)
        query = await address_manager.delete_address(int(idx))
        assert query is True
