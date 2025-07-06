from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.main import City
import logging
from typing import Sequence
from html import escape


class CityManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_city(self, name: str) -> City | None:
        """
        Creates a new city.
        :param name:
        :return:
        """
        try:
            city_ = City(name=name)
            self.session.add(city_)
            await self.session.commit()
            return city_
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return None

    async def get_city(self, idx: int) -> City | None:
        """
        Gets a city.
        :param idx:
        :return:
        """
        try:
            query = select(City).where(City.id == idx)
            result = await self.session.execute(query)
            city_ = result.scalar_one_or_none()
            if city_ is None:
                return None
            return city_
        except Exception as e:
            logging.exception(e)
            return None

    async def update_city(self,
                          idx: int,
                          name: str
                          ) -> bool:
        """
        Updates a city.
        :param idx:
        :param name:
        :return:
        """
        try:
            query = select(City).where(City.id == idx)
            result = await self.session.execute(query)
            city_ = result.scalar_one_or_none()
            if city_ is None:
                return False
            city_.name = escape(str(name))
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
