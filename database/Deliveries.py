from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.main import Delivery
import logging
from typing import Sequence
from html import escape


class DeliveryManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_delivery(self, name, city, address) -> bool:
        """
        Creates a delivery and returns True if it was created.
        :param name:
        :param city:
        :param address:
        :return:
        """
        try:
            delivery = Delivery(name=name, city=city, address=address)
            self.session.add(delivery)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return False

    async def get_delivery(self, idx: int) -> Delivery | None:
        """
        Gets a delivery and returns it if it was created.
        :param idx:
        :return:
        """
        try:
            query = select(Delivery).where(Delivery.id == idx)
            result = await self.session.execute(query)
            delivery = result.scalar_one_or_none()
            if delivery is None:
                return None
            return delivery
        except Exception as e:
            logging.exception(e)
            return None

    async def update_delivery(self,  idx: int, name: str,
                              city: str, address: str) -> bool:
        try:
            query = select(Delivery).where(Delivery.id == idx)
            result = await self.session.execute(query)
            delivery = result.scalar_one_or_none()
            if delivery is None:
                return False
            delivery.name = escape(str(name))
            delivery.city = escape(str(city))
            delivery.address = escape(str(address))
            await self.session.commit()
            return True
        except Exception as e:
            logging.exception(e)
            return False

    async def get_deliveries(self) -> Sequence[Delivery] | None:
        """
        Gets all deliveries and returns them if they were created.
        :return:
        """
        try:
            query = select(Delivery)
            result = await self.session.execute(query)
            return result.scalars().all()
        except Exception as e:
            logging.exception(e)
            return None

    async def delete_delivery(self, idx: int) -> bool:
        """
        Deletes a delivery and returns True if it was deleted.
        :param idx:
        :return:
        """
        try:
            query = select(Delivery).where(Delivery.id == idx)
            result = await self.session.execute(query)
            delivery = result.scalar_one_or_none()
            if delivery is None:
                return False
            await self.session.delete(delivery)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return False
