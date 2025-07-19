import pytest
from database.Address import AddressManager
from database.main import async_session_maker, Address


@pytest.mark.asyncio
async def test_create_address():
    async with async_session_maker() as session:
        address_manager = AddressManager(session)
        await address_manager.create_address(
            name="Address1",
            city_id=1)
        address = await address_manager.create_address(
            name="Address2",
            city_id=2)
        assert isinstance(address, Address)
        address = await address_manager.create_address(
            name="Address2",
            city_id=0)
        assert address is None


@pytest.mark.asyncio
async def test_get_address():
    async with async_session_maker() as session:
        address_manager = AddressManager(session)
        addresses = await address_manager.get_address(city_id=1)
        assert isinstance(addresses, list)
        for address in addresses:
            assert address.name == "Address1"


@pytest.mark.asyncio
async def test_update_address():
    async with async_session_maker() as session:
        address_manager = AddressManager(session)
        address = await address_manager.update_address(
            idx=1,
            name="Address3",
            city_id=2
        )
        assert address is True
        address = await address_manager.update_address(
            idx=2,
            name="Address4",
            city_id=1
        )
        assert address is True
        address = await address_manager.update_address(
            idx=0,
            name="Address4",
            city_id=1
        )
        assert address is False


@pytest.mark.asyncio
async def test_get_addresses():
    async with async_session_maker() as session:
        address_manager = AddressManager(session)
        addresses = await address_manager.get_addresses()
        for address in addresses:
            assert address.name in ["Address3", "Address4"]
            assert address.city_id in [1, 2]


@pytest.mark.asyncio
async def test_delete_address():
    async with async_session_maker() as session:
        address_manager = AddressManager(session)
        query = await address_manager.delete_address(1)
        assert query is True
        query = await address_manager.delete_address(2)
        assert query is True
