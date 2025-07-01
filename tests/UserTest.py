from helps.help import hash_password
import pytest
from database.User import UserManager
from database.main import async_session_maker


@pytest.mark.asyncio
async def test_create_user():
    async with async_session_maker() as session:
        user_manager = UserManager(session)
        user = await user_manager.create_user(
            username="Alex",
            password="12345678",
            phone="8000000000",
            email="admin@admin.com"
        )
        assert user is not False


@pytest.mark.asyncio
async def test_update_user():
    async with async_session_maker() as session:
        user_manager = UserManager(session)
        user = await user_manager.update_user(idx=1, password="0000")
        assert user is not False


@pytest.mark.asyncio
async def test_set_status():
    async with async_session_maker() as session:
        user_manager = UserManager(session)
        user = await user_manager.set_status(1, 0)
        assert user is True


@pytest.mark.asyncio
async def test_add_comments():
    async with async_session_maker() as session:
        user_manager = UserManager(session)
        user = await user_manager.add_comments(1, "TEST")
        assert user is True


@pytest.mark.asyncio
async def test_resset_password():
    async with async_session_maker() as session:
        user_manager = UserManager(session)
        user = await user_manager.reset_password(1)
        assert user is True


@pytest.mark.asyncio
async def test_get_user():
    async with async_session_maker() as session:
        user_manager = UserManager(session)
        query = await user_manager.get_user(1)
        assert query.username == "Alex"
        assert query.email is not None
        assert query.phone == "8000000000"
        assert query.status == 0
        assert query.password == hash_password("0000")
        assert query.comments == "TEST"


@pytest.mark.asyncio
async def test_get_users():
    async with async_session_maker() as session:
        user_manager = UserManager(session)
        users = await user_manager.get_users()
        for user in users:
            assert user.username == "Alex"


@pytest.mark.asyncio
async def test_get_user_by_username():
    async with async_session_maker() as session:
        user_manager = UserManager(session)
        query = await user_manager.get_user_by_username(
            username="Alex",
            password="0000"
        )
        assert query.username == "Alex"


@pytest.mark.asyncio
async def test_delete_user():
    async with (async_session_maker() as session):
        user_manager = UserManager(session)
        query = await user_manager.delete_user(1)
        assert query is True
