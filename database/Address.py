from sqlalchemy import Row, RowMapping
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.main import Address, City
import logging
from typing import Sequence, Any
from html import escape
from sqlalchemy import text


class AddressManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_address(self, name: str, city_id: int) -> Address | None:
        """
        Creates a new address.
        :param name:
        :param city_id:
        :return:
        """
        try:
            if city_id <= 0:
                return None
            address_ = Address(name=name, city_id=city_id)
            self.session.add(address_)
            await self.session.commit()
            return address_
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return None

    async def get_address(
            self,
            city_id: int
    ) -> Sequence[Row[Any] | RowMapping | Any] | None:
        """
        Gets address.
        :param city_id:
        :return:
        """
        try:
            if city_id <= 0:
                return None
            query = (select(Address)
                     .join(City, City.id == Address.city_id)
                     .where(Address.city_id == city_id))
            result = await self.session.execute(query)
            address_ = result.scalars().all()
            return address_
        except Exception as e:
            logging.exception(e)
            return None

    async def update_address(self,
                             idx: int,
                             name: str,
                             city_id: int
                             ) -> bool:
        """
        Updates address.
        :param idx:
        :param name:
        :param city_id:
        :return:
        """
        try:
            if city_id <= 0:
                return False
            query = select(Address).where(Address.id == idx)
            result = await self.session.execute(query)
            address_ = result.scalar_one_or_none()
            if address_ is None:
                return False
            address_.name = escape(str(name))
            address_.city_id = int(city_id)
            await self.session.commit()
            return True
        except Exception as e:
            logging.exception(e)
            return False

    async def get_addresses(self) -> Sequence[Address] | None:
        """
        Gets all addresses.
        :return:
        """
        try:
            query = select(Address)
            result = await self.session.execute(query)
            return result.scalars().all()
        except Exception as e:
            logging.exception(e)
            return None

    async def delete_address(self, idx: int) -> bool:
        """
        Deletes address.
        :param idx:
        :return:
        """
        try:
            query = select(Address).where(Address.id == idx)
            result = await self.session.execute(query)
            address_ = result.scalar_one_or_none()
            if address_ is None:
                return False
            await self.session.delete(address_)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return False

    async def truncate_posts_addresses(self) -> bool:
        """
        Truncate the addresses table
        """
        try:
            await self.session.execute(text("DELETE FROM addresses"))
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return False
