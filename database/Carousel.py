from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from html import escape
from database.main import Carousel
import logging
from typing import Sequence


class CarouselManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_item(self, title: str, description: str,
                          image: str) -> bool:
        """
        Creates a new carousel item.
        :param title:
        :param description:
        :param image:
        :return:
        """
        try:
            title = escape(str(title))
            description = escape(str(description))
            image = escape(str(image))
            carousel = Carousel(title=title, description=description,
                                image=image)
            self.session.add(carousel)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return False

    async def update_item(self, idx: int, title: str, description: str,
                          image: str) -> bool:
        """
        Updates a carousel item.
        :param idx:
        :param title:
        :param description:
        :param image:
        :return:
        """
        try:
            query = select(Carousel).where(Carousel.id == idx)
            result = await self.session.execute(query)
            carousel = result.scalar_one_or_none()
            if carousel is None:
                return False
            carousel.title = title
            carousel.description = escape(str(description))
            carousel.image = escape(str(image))
            await self.session.commit()
            return True
        except Exception as e:
            logging.exception(e)
            return False

    async def get_items(self) -> Sequence[Carousel] | None:
        """
        Gets all carousel items.
        :return:
        """
        try:
            query = select(Carousel)
            result = await self.session.execute(query)
            return result.scalars().all()
        except Exception as e:
            logging.exception(e)
            return None

    async def delete_items(self, idx: int) -> bool:
        """
        Deletes all carousel items.
        :param idx:
        :return:
        """
        try:
            query = select(Carousel).where(Carousel.id == idx)
            result = await self.session.execute(query)
            carousel = result.scalar_one_or_none()
            if carousel is None:
                return False
            await self.session.delete(carousel)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return False
