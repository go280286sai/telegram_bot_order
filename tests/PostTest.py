import pytest
from database.Post import PostManager
from database.main import async_session_maker




@pytest.mark.asyncio
async def test_create_post():
    async with async_session_maker() as session:
        post_manager = PostManager(session)
        delivery = await post_manager.create_post(
            name="Post")
        assert delivery is True


@pytest.mark.asyncio
async def test_get_post():
    async with async_session_maker() as session:
        post_manager = PostManager(session)
        query = await post_manager.get_post(1)
        assert query.name == "Post"


@pytest.mark.asyncio
async def test_update_post():
    async with async_session_maker() as session:
        post_manager = PostManager(session)
        delivery = await post_manager.update_post(
            idx=1,
            name="Post" + "1",
        )
        assert delivery is True

@pytest.mark.asyncio
async def test_get_posts():
    async with async_session_maker() as session:
        post_manager = PostManager(session)
        posts = await post_manager.get_posts()
        for post in posts:
            assert post.name == "Post" + "1"


@pytest.mark.asyncio
async def test_delete_post():
    async with async_session_maker() as session:
        delivery_manager = PostManager(session)
        query = await delivery_manager.delete_post(1)
        assert query is True
