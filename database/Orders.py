from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.main import Order, Product, User, Delivery
import logging
from typing import Sequence
from datetime import datetime

class OrderManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_order(self, products: str, user_id: int,
                           delivery_id: int, total: float, transaction_id: str) -> bool:
        """
        Create a new order
        :param transaction_id:
        :param products:
        :param user_id:
        :param delivery_id:
        :param total:
        :return:
        """
        try:
            order = Order(
                products=str(products),
                user_id=int(user_id),
                delivery_id=int(delivery_id),
                total=float(total),
                transaction_id=str(transaction_id))
            self.session.add(order)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return False

    async def get_order(self, idx: int) -> Order | None:
        """
        Get a specific order
        :param idx:
        :return:
        """
        try:
            query = (select(Order, Product.name)
                     .join(User, Order.user_id == User.id)
                     .join(Delivery, Order.delivery_id == Delivery.id)
                     .where(Order.id == idx))
            result = await self.session.execute(query)
            return result.scalar()
        except Exception as e:
            logging.exception(e)
            return None

    async def set_status(self, idx: int, status: int) -> bool:
        """
        Set a status of a specific order
        :param idx:
        :param status:
        :return:
        """
        try:
            query = select(Order).where(Order.id == idx)
            result = await self.session.execute(query)
            order = result.scalar_one()
            order.status = status
            await self.session.commit()
            return True
        except Exception as e:
            logging.error(e)
            return False

    async def get_orders(self) -> Sequence[Order] | None:
        """
        Get all orders
        :return:
        """
        try:
            query = (select(Order, Product.name)
                     .join(User, Order.user_id == User.id)
                     .join(Delivery, Order.delivery_id == Delivery.id))
            result = await self.session.execute(query)
            return result.scalars().all()
        except Exception as e:
            logging.error(e)
            return None

    async def get_orders_user(self, idx: int):
        """
        Get all orders for a specific user
        :param idx:
        :return:
        """
        try:
            query = (select(Order)
                     .where(Order.user_id == idx))
            orders = await self.session.execute(query)
            result = orders.scalars().all()
            orders_ = [{
                "id": p.id,
                "total": p.total,
                "status": p.status,
                "created_at": p.created_at.strftime("%Y-%m-%d"),
            }
                for p in result
            ]
            return orders_
        except Exception as e:
            logging.exception(e)
            return None

    async def delete_order(self, idx: int) -> bool:
        """
        Delete a specific order
        :param idx:
        :return:
        """
        try:
            query = select(Order).where(Order.id == idx)
            result = await self.session.execute(query)
            order = result.scalar_one_or_none()
            if order is None:
                return False
            await self.session.delete(order)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return False
