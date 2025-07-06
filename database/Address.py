from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.main import Address
import logging
from typing import Sequence
from html import escape


class AddressManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_address(self, name: str) -> Address | None:
        """
        Creates a new address.
        :param name:
        :return:
        """
        try:
            address_ = Address(name=name)
            self.session.add(address_)
            await self.session.commit()
            return address_
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return None

    async def get_address(self, idx: int) -> Address | None:
        """
        Gets address.
        :param idx:
        :return:
        """
        try:
            query = select(Address).where(Address.id == idx)
            result = await self.session.execute(query)
            address_ = result.scalar_one_or_none()
            if address_ is None:
                return None
            return address_
        except Exception as e:
            logging.exception(e)
            return None

    async def update_address(self,
                             idx: int,
                             name: str
                             ) -> bool:
        """
        Updates address.
        :param idx:
        :param name:
        :return:
        """
        try:
            query = select(Address).where(Address.id == idx)
            result = await self.session.execute(query)
            address_ = result.scalar_one_or_none()
            if address_ is None:
                return False
            address_.name = escape(str(name))
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
