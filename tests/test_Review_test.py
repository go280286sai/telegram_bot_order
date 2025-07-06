import pytest
from database.main import async_session_maker, Review
from database.Review import ReviewManager


@pytest.mark.asyncio
async def test_create_review():
    async with async_session_maker() as session:
        review_manager = ReviewManager(session)
        query = await review_manager.create_review(
            name="Author",
            text="I love Python",
            gender=1
        )
        assert isinstance(query, Review)


@pytest.mark.asyncio
async def test_update_review():
    async with async_session_maker() as session:
        review_manager = ReviewManager(session)
        query = await review_manager.update_review(
            idx=1,
            name="AuthorNew",
            text="I love Python very well",
            gender=0
        )
        assert query is True


@pytest.mark.asyncio
async def test_get_reviews():
    async with async_session_maker() as session:
        review_manager = ReviewManager(session)
        reviews = await review_manager.get_reviews()
        for review in reviews:
            assert review.name == "AuthorNew"
            assert review.text == "I love Python very well"
            assert review.gender == 0


@pytest.mark.asyncio
async def test_delete_review():
    async with async_session_maker() as session:
        review_manager = ReviewManager(session)
        query = await review_manager.delete_review(1)
        assert query is True
