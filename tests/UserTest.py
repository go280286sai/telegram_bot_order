import sys

sys.path.append("D:/dev/python/projects/bot_order")

import pytest
from database.User import UserManager
from database.main import async_session_maker
from helps.help import hash_password

@pytest.mark.asyncio
async def test_create_user():
    async with async_session_maker() as session:
        user_manager = UserManager(session)
        user = await user_manager.create_user("Alex", "12345678")
        assert user == True


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
async def test_delete_user():
    async with async_session_maker() as session:
        user_manager = UserManager(session)
        query = await user_manager.delete_user(1)
        assert query is True
