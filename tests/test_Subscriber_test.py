import pytest
from database.main import async_session_maker
from database.Subscriber import SubscriberManager
from helps.helper import generate_transaction

hash_val = generate_transaction()


@pytest.mark.asyncio
async def test_create_subscriber():
    async with async_session_maker() as session:
        subscribe_manager = SubscriberManager(session)
        query = await subscribe_manager.create_subscriber(
            email="admin@admin.ua",
            hash_active=hash_val
        )
        assert query is not False


@pytest.mark.asyncio
async def test_get_subscriber():
    async with async_session_maker() as session:
        subscribe_manager = SubscriberManager(session)
        queries = await subscribe_manager.get_subscribers()
        assert queries is not None
        for query in queries:
            assert query['email'] == "admin@admin.ua"


@pytest.mark.asyncio
async def test_set_active_subscriber():
    async with async_session_maker() as session:
        subscribe_manager = SubscriberManager(session)
        query = await subscribe_manager.set_active_subscriber(
            idx=1,
            hash_active=hash_val
        )
        assert query is True
        query = await subscribe_manager.set_active_subscriber(
            idx=0,
            hash_active=hash_val
        )
        assert query is False


@pytest.mark.asyncio
async def test_get_active_subscriber():
    async with async_session_maker() as session:
        subscribe_manager = SubscriberManager(session)
        queries = await subscribe_manager.get_active_subscribers()
        assert queries is not None
        for query in queries:
            assert query['email'] == "admin@admin.ua"


@pytest.mark.asyncio
async def test_set_destroy_subscriber():
    async with async_session_maker() as session:
        subscribe_manager = SubscriberManager(session)
        destroy = await subscribe_manager.get_hashed_destroy(1)
        assert destroy is not None
        query = await subscribe_manager.set_destroy_subscriber(
            idx=1,
            hash_destroy=destroy
        )
        assert query is True
        query = await subscribe_manager.set_destroy_subscriber(
            idx=0,
            hash_destroy=destroy
        )
        assert query is False


@pytest.mark.asyncio
async def test_delete_subscriber():
    async with async_session_maker() as session:
        subscribe_manager = SubscriberManager(session)
        query = await subscribe_manager.delete_subscriber(1)
        assert query is False


@pytest.mark.asyncio
async def test_truncate_user():
    async with async_session_maker() as session:
        user_manager = SubscriberManager(session)
        query = await user_manager.truncate_subscribers_table()
        assert query is True
