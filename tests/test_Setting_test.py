import pytest
from database.Setting import SettingManager
from database.main import async_session_maker, Setting
import pytest_asyncio


@pytest_asyncio.fixture()
async def test_create_setting():
    async with async_session_maker() as session:
        setting_manager = SettingManager(session)
        setting = await setting_manager.create_setting(
            name="Title",
            value="Value", )
        assert isinstance(setting, Setting)
        return setting.id


@pytest_asyncio.fixture
async def test_get_setting(test_create_setting):
    async with async_session_maker() as session:
        idx = test_create_setting
        setting_manager = SettingManager(session)
        query = await setting_manager.get_setting(int(idx))
        assert query.name == "Title"
        query = await setting_manager.get_setting(0)
        assert query is None
        return idx


@pytest_asyncio.fixture
async def test_update_setting(test_get_setting):
    async with async_session_maker() as session:
        idx = test_get_setting
        setting_manager = SettingManager(session)
        setting = await setting_manager.update_setting(
            idx=idx,
            name="Title1",
            value="Value1",
        )
        assert setting is True
        setting = await setting_manager.update_setting(
            idx=0,
            name="Title1",
            value="Value1",
        )
        assert setting is False
        return idx


@pytest.mark.asyncio
async def test_get_settings():
    async with async_session_maker() as session:
        setting_manager = SettingManager(session)
        settings = await setting_manager.get_settings()
        for setting in settings:
            assert setting.name == "Title1"


@pytest.mark.asyncio
async def test_delete_setting(test_update_setting):
    async with async_session_maker() as session:
        idx = test_update_setting
        setting_manager = SettingManager(session)
        query = await setting_manager.delete_setting(int(idx))
        assert query is True
        query = await setting_manager.delete_setting(int(idx))
        assert query is False


@pytest.mark.asyncio
async def test_truncate_user():
    async with async_session_maker() as session:
        user_manager = SettingManager(session)
        query = await user_manager.truncate_settings_table()
        assert query is True
