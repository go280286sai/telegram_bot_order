import pytest_asyncio

from helps.help import hash_password, generate_transaction
import pytest
from database.User import UserManager
from database.main import async_session_maker, User
from helps.Middleware import is_admin


@pytest.mark.asyncio
async def test_create_user():
    async with async_session_maker() as session:
        user_manager = UserManager(session)
        user = await user_manager.create_user(
            username="Alex",
            password="12345678",
            phone="8000000000",
            email="admin@admin.com",
            hash_active=generate_transaction()
        )
        assert isinstance(user, User)


@pytest.mark.asyncio
async def test_is_admin():
    user = await is_admin(1)
    assert isinstance(user, bool)
    assert user is False


@pytest.mark.asyncio
async def test_update_user():
    async with async_session_maker() as session:
        user_manager = UserManager(session)
        user = await user_manager.update_user(idx=1, password="0000")
        await user_manager.set_admin(user_id=1, status=1)
        assert user is not False
        assert user.password == hash_password('0000')


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


@pytest_asyncio.fixture
async def test_resset_password():
    async with async_session_maker() as session:
        user_manager = UserManager(session)
        user = await user_manager.reset_password(1)
        assert isinstance(user, str)
        return user


@pytest_asyncio.fixture
async def test_get_user(test_resset_password):
    async with async_session_maker() as session:
        password = str(test_resset_password)
        user_manager = UserManager(session)
        query = await user_manager.get_user(1)
        assert isinstance(query, User)
        assert query.username is not None
        assert query.email is not None
        assert query.phone == "8000000000"
        assert query.status == 0
        assert query.password == hash_password(password)
        assert query.comments == "TEST"
        return password


@pytest.mark.asyncio
async def test_get_users():
    async with async_session_maker() as session:
        user_manager = UserManager(session)
        users = await user_manager.get_users()
        for user in users:
            assert user['username'] == "Alex"


@pytest.mark.asyncio
async def test_get_user_by_username(test_get_user):
    password = str(test_get_user)
    async with async_session_maker() as session:
        user_manager = UserManager(session)
        query = await user_manager.get_user_by_username(
            username="Alex",
            password=password
        )
        assert query.username == "Alex"


@pytest.mark.asyncio
async def test_set_hashed_active_for_delete():
    async with async_session_maker() as session:
        user_manager = UserManager(session)
        query = await user_manager.set_hashed_active_for_delete(
            idx="1",
            hashed_active="qwerty123"
        )
        assert query is not None
        query = await user_manager.set_hashed_active_for_delete(
            idx="0",
            hashed_active="qwerty123"
        )
        assert query is None


@pytest.mark.asyncio
async def test_get_user_by_username_email():
    async with async_session_maker() as session:
        user_manager = UserManager(session)
        query = await user_manager.get_user_by_username_email(
            username="Alex",
            email="admin@admin.com"
        )
        assert isinstance(query, User)
        query = await user_manager.get_user_by_username_email(
            username="Alex2",
            email="admin@admin.com"
        )
        assert query is None
        query = await user_manager.get_user_by_username_email(
            username="Alex",
            email="admin@admin.com2"
        )
        assert query is None


@pytest.mark.asyncio
async def test_delete_user(test_get_user):
    password = str(test_get_user)
    async with async_session_maker() as session:
        user_manager = UserManager(session)
        query = await user_manager.get_user_by_username(
            username="Alex",
            password=password
        )
        assert query.username == "Alex"
        user_ = await user_manager.delete_user(query.id)
        assert user_ is True
