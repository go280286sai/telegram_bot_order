from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.main import Delivery
import logging
from typing import Sequence
from html import escape

logging.basicConfig(level=logging.INFO)


class DeliveryManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_delivery(self, name, city, address) -> bool:
        try:
            delivery = Delivery(name=name, city=city, address=address)
            self.session.add(delivery)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logging.error(e)
            return False

    async def get_delivery(self, id: str) -> Delivery | None:
        try:
            query = select(Delivery).where(Delivery.id == id)
            result = await self.session.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            logging.error(e)
            return None

    async def update_delivery(self, id: int, name: str, city: str, address: str) -> bool | None:
        try:
            query = select(Delivery).where(Delivery.id == id)
            result = await self.session.execute(query)
            delivery = result.scalar()
            delivery.name = escape(str(name))
            delivery.city = escape(str(city))
            delivery.address = escape(str(address))
            await self.session.commit()
            return True
        except Exception as e:
            logging.error(e)
            return None

    async def get_deliveries(self) -> Sequence[Delivery] | None:
        try:
            query = select(Delivery)
            result = await self.session.execute(query)
            return result.scalars().all()
        except Exception as e:
            logging.error(e)
            return None

    async def delete_delivery(self, id: str) -> bool:
        try:
            query = select(Delivery).where(Delivery.id == id)
            result = await self.session.execute(query)
            delivery = result.scalar_one_or_none()  # Get the actual user object

            if delivery:
                await self.session.delete(delivery)
                await self.session.commit()
                return True

            return False  # User not found
        except Exception as e:
            await self.session.rollback()  # Ensure rollback on failure
            logging.error(e)
            return False
