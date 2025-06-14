from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.main import Order
import logging
from typing import Sequence

logging.basicConfig(level=logging.INFO)


class OrderManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_order(self, product_id: int, user_id: id) -> bool:
        try:
            order = Order(product_id=int(product_id), user_id=int(user_id))
            self.session.add(order)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logging.error(e)
            return False

    async def get_order(self, id: str) -> Order | None:
        try:
            query = select(Order).where(Order.id == id)
            result = await self.session.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            logging.error(e)
            return None

    async def set_status(self, id: int, status: int) -> bool:
        try:
            query = select(Order).where(Order.id == id)
            result = await self.session.execute(query)
            order = result.scalar()
            order.status = status
            await self.session.commit()
            return True
        except Exception as e:
            logging.error(e)
            return None

    async def get_orders(self) -> Sequence[Order] | None:
        try:
            query = select(Order)
            result = await self.session.execute(query)
            return result.scalars().all()
        except Exception as e:
            logging.error(e)
            return None

    async def delete_order(self, id: str) -> bool:
        try:
            query = select(Order).where(Order.id == id)
            result = await self.session.execute(query)
            order = result.scalar_one_or_none()  # Get the actual user object

            if order:
                await self.session.delete(order)
                await self.session.commit()
                return True

            return False  # User not found
        except Exception as e:
            await self.session.rollback()  # Ensure rollback on failure
            logging.error(e)
            return False
