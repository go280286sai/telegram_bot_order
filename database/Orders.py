from datetime import datetime
from typing import Any, Optional

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.main import Order, User, Post, City, Address
import logging
from html import escape
from sqlalchemy import text

from helps.predict import Predict


class OrderManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_order(self,
                           products: str,
                           user_id: int,
                           delivery: str,
                           total: float,
                           transaction_id: str,
                           bonus: int = 0,
                           discount: int = 0,
                           ) -> bool:
        """
        Create a new order
        :param discount:
        :param bonus:
        :param transaction_id:
        :param products:
        :param user_id:
        :param delivery:
        :param total:
        :return:
        """
        try:
            order = Order(
                products=str(products),
                user_id=int(user_id),
                delivery=str(delivery),
                total=float(total),
                transaction_id=str(transaction_id),
                discount=int(discount),
                bonus=int(bonus))
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
            query = (select(Order)
                     .join(User, Order.user_id == User.id)
                     .where(Order.id == int(idx)))
            result = await self.session.execute(query)
            return result.scalar_one_or_none()
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
            if status not in [0, 1]:
                return False
            query = select(Order).where(Order.id == idx)
            result = await self.session.execute(query)
            order = result.scalar_one()
            order.status = status
            await self.session.commit()
            return True
        except Exception as e:
            logging.error(e)
            return False

    async def get_orders(self) -> list | None:
        """
        Get all orders
        :return:
        """
        try:
            query = select(Order)
            result = await self.session.execute(query)
            orders = result.scalars().all()
            orders_ = [
                {
                    "id": p.id,
                    "products": p.products,
                    "user": p.user_id,
                    "delivery": p.delivery,
                    "total": p.total,
                    "transaction_id": p.transaction_id,
                    "status": p.status,
                    "invoice": p.invoice,
                    "comment": p.comment,
                    "created_at": p.created_at.strftime("%d-%m-%Y"),
                } for p in orders
            ]
            return orders_
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
                     .join(User, Order.user_id == User.id)
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

    async def set_invoice_order(self, idx: int, invoice: str) -> bool:
        """
        Set an invoice order for a specific order
        :param idx:
        :param invoice:
        :return:
        """
        try:
            query = (select(Order)
                     .where(Order.id == idx))
            order = await self.session.execute(query)
            result = order.scalar_one_or_none()
            if result is None:
                return False
            result.invoice = escape(invoice)
            result.status = 1
            await self.session.commit()
            return True
        except Exception as e:
            logging.exception(e)
            return False

    async def add_comment(self, idx: int, comment: str) -> bool:
        """
        Set an invoice order for a specific order
        :param idx:
        :param comment:
        :return:
        """
        try:
            query = (select(Order)
                     .where(Order.id == idx))
            order = await self.session.execute(query)
            result = order.scalar_one_or_none()
            if result is None:
                return False
            result.comment = escape(comment)
            await self.session.commit()
            return True
        except Exception as e:
            logging.exception(e)
            return False

    async def get_predict(self, term: int = 0) -> list[Any] | None:
        """
        Get predict data for a specific order
        :return:
        """
        try:
            query = select(Order.total.label("total"),
                           Order.created_at.label("created_at"))
            result = await self.session.execute(query)
            orders = result.all()
            data = [
                list(el) for el in orders
            ]
            predict = Predict(term=term)
            results: Optional[
                list[tuple[float, datetime]]
            ] = predict.build(data=data)
            return results
        except Exception as e:
            logging.error(e)
            return None

    async def get_delivery(
            self,
            post_id: int,
            city_id: int,
            address_id: int
    ) -> dict | None:
        """
        Gets a delivery and returns it if it was created.
        :param post_id:
        :param city_id:
        :param address_id:
        :return:
        """
        try:
            query = (
                select(Post.name.label("name"),
                       City.name.label("city"),
                       Address.name.label("address"))
                .join(City, Post.id == City.post_id)
                .join(Address, City.id == Address.city_id)
                .where(Post.id == post_id)
                .where(City.id == city_id)
                .where(Address.id == address_id)
            )

            result = await self.session.execute(query)
            rows = result.all()
            if not rows:
                return None
            return [
                {
                    "post_name": post_name,
                    "city_name": city_name,
                    "address_name": address_name
                }
                for post_name, city_name, address_name in rows
            ][0]
        except Exception as e:
            logging.exception(e)
            return None

    async def truncate_orders_table(self) -> bool:
        """
        Truncate the orders table
        """
        try:
            await self.session.execute(text("DELETE FROM orders"))
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return False
