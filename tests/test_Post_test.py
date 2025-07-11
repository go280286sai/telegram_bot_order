import pytest
from database.Post import PostManager
from database.main import async_session_maker, Post
import pytest_asyncio


@pytest_asyncio.fixture()
async def test_create_post():
    async with async_session_maker() as session:
        post_manager = PostManager(session)
        post = await post_manager.create_post(
            name="NewPost")
        assert isinstance(post, Post)
        return post.id


@pytest_asyncio.fixture
async def test_get_post(test_create_post):
    async with async_session_maker() as session:
        idx = test_create_post
        post_manager = PostManager(session)
        query = await post_manager.get_post(int(idx))
        assert query.name == "NewPost"
        return idx


@pytest_asyncio.fixture
async def test_update_post(test_get_post):
    async with async_session_maker() as session:
        idx = test_get_post
        post_manager = PostManager(session)
        post = await post_manager.update_post(
            idx=int(idx),
            name="NewPost1",
        )
        assert post is True
        return idx


@pytest.mark.asyncio
async def test_get_posts():
    async with async_session_maker() as session:
        post_manager = PostManager(session)
        posts = await post_manager.get_posts()
        for post in posts:
            assert post.name == "NewPost1"


@pytest.mark.asyncio
async def test_delete_post(test_update_post):
    async with async_session_maker() as session:
        idx = test_update_post
        post_manager = PostManager(session)
        query = await post_manager.delete_post(int(idx))
        assert query is True
