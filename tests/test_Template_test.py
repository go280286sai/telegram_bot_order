import pytest
from database.main import async_session_maker
from database.Template import TemplateManager


@pytest.mark.asyncio
async def test_create_template():
    async with async_session_maker() as session:
        tmp_manager = TemplateManager(session)
        email = await tmp_manager.create_template(
            header="Very cool template",
            title="Very impotent template",
            body="Here is some body"
            )
        assert email is True


@pytest.mark.asyncio
async def test_update_template():
    async with async_session_maker() as session:
        tmp_manager = TemplateManager(session)
        query = await tmp_manager.update_template(
            idx=1,
            header="Very cool template2",
            title="Very impotent template2",
            body="Here is some body2"
        )
        assert query is True
        query = await tmp_manager.update_template(
            idx=0,
            header="Very cool template2",
            title="Very impotent template2",
            body="Here is some body2"
        )
        assert query is False


@pytest.mark.asyncio
async def test_get_template():
    async with async_session_maker() as session:
        tmp_manager = TemplateManager(session)
        query = await tmp_manager.get_template(1)
        assert query.header == "Very cool template2"
        assert query.title == "Very impotent template2"
        assert query.body == "Here is some body2"
        query = await tmp_manager.get_template(0)
        assert query is None


@pytest.mark.asyncio
async def test_get_templates():
    async with async_session_maker() as session:
        tmp_manager = TemplateManager(session)
        emails = await tmp_manager.get_templates()
        for email in emails:
            assert email.header == "Very cool template2"
            assert email.title == "Very impotent template2"
            assert email.body == "Here is some body2"


@pytest.mark.asyncio
async def test_delete_template():
    async with async_session_maker() as session:
        tmp_manager = TemplateManager(session)
        query = await tmp_manager.delete_template(1)
        assert query is True
