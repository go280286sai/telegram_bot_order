import pytest
from database.Address import AddressManager
from database.main import async_session_maker


@pytest.mark.asyncio
async def test_create_address():
    async with async_session_maker() as session:
        address_manager = AddressManager(session)
        address = await address_manager.create_address(
            name="Address")
        assert address is True


@pytest.mark.asyncio
async def test_get_address():
    async with async_session_maker() as session:
        address_manager = AddressManager(session)
        query = await address_manager.get_address(1)
        assert query.name == "Address"


@pytest.mark.asyncio
async def test_update_address():
    async with async_session_maker() as session:
        address_manager = AddressManager(session)
        address = await address_manager.update_address(
            idx=1,
            name="Address" + "1",
        )
        assert address is True


@pytest.mark.asyncio
async def test_get_addresses():
    async with async_session_maker() as session:
        address_manager = AddressManager(session)
        addresses = await address_manager.get_addresses()
        for address in addresses:
            assert address.name == "Address" + "1"


@pytest.mark.asyncio
async def test_delete_address():
    async with async_session_maker() as session:
        address_manager = AddressManager(session)
        query = await address_manager.delete_address(1)
        assert query is True
