import pytest
from database.main import async_session_maker
from database.Carousel import CarouselManager


@pytest.mark.asyncio
async def test_create_carousel():
    async with async_session_maker() as session:
        carousel_manager = CarouselManager(session)
        query = await carousel_manager.create_item(
            title="Image",
            description="Description",
            image="https://example.com",
        )
        assert query is True


@pytest.mark.asyncio
async def test_update_carousel():
    async with async_session_maker() as session:
        carousel_manager = CarouselManager(session)
        query = await carousel_manager.update_item(
            idx=1,
            title="ImageNew",
            description="Description 2",
            image="https://example.org",
        )
        assert query is True
        query = await carousel_manager.update_item(
            idx=0,
            title="ImageNew",
            description="Description 2",
            image="https://example.org",
        )
        assert query is False


@pytest.mark.asyncio
async def test_get_carousels():
    async with async_session_maker() as session:
        carousel_manager = CarouselManager(session)
        carousels = await carousel_manager.get_items()
        for carousel in carousels:
            assert carousel.title == "ImageNew"
            assert carousel.description == "Description 2"
            assert carousel.image == "https://example.org"


@pytest.mark.asyncio
async def test_delete_carousel():
    async with async_session_maker() as session:
        carousel_manager = CarouselManager(session)
        query = await carousel_manager.delete_items(1)
        assert query is True
