from sqlalchemy import Row, RowMapping
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.main import City, Post
import logging
from typing import Sequence, Any
from html import escape


class CityManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_city(self, name: str, post_id) -> City | None:
        """
        Creates a new city.
        :param name:
        :param post_id:
        :return:
        """
        try:
            if post_id <= 0:
                return None
            city_ = City(name=name, post_id=post_id)
            self.session.add(city_)
            await self.session.commit()
            return city_
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return None

    async def get_city(
            self,
            post_id: int
    ) -> Sequence[Row[Any] | RowMapping | Any] | None:
        """
        Gets a city.
        :param post_id:
        :return:
        """
        try:
            if post_id <= 0:
                return None
            query = (select(City)
                     .join(Post, City.post_id == Post.id)
                     .where(City.post_id == int(post_id)))
            result = await self.session.execute(query)
            city_ = result.scalars().all()
            if city_ is None:
                return None
            return city_
        except Exception as e:
            logging.exception(e)
            return None

    async def update_city(self,
                          idx: int,
                          name: str,
                          post_id: int,
                          ) -> bool:
        """
        Updates a city.
        :param post_id:
        :param idx:
        :param name:
        :return:
        """
        try:
            if post_id <= 0 or idx <= 0:
                return False
            query = select(City).where(City.id == idx)
            result = await self.session.execute(query)
            city_ = result.scalar_one_or_none()
            if city_ is None:
                return False
            city_.name = escape(str(name))
            city_.post_id = int(post_id)
            await self.session.commit()
            return True
        except Exception as e:
            logging.exception(e)
            return False

    async def get_cities(self) -> Sequence[City] | None:
        """
        Gets all cities.
        :return:
        """
        try:
            query = select(City)
            result = await self.session.execute(query)
            return result.scalars().all()
        except Exception as e:
            logging.exception(e)
            return None

    async def delete_city(self, idx: int) -> bool:
        """
        Deletes a city.
        :param idx:
        :return:
        """
        try:
            query = select(City).where(City.id == idx)
            result = await self.session.execute(query)
            city_ = result.scalar_one_or_none()
            if city_ is None:
                return False
            await self.session.delete(city_)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return False
