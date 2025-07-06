from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.main import Delivery, Post, City, Address
import logging


class DeliveryManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_delivery(self,
                              post_id: int,
                              city_id: int,
                              address_id: int
                              ) -> bool | Delivery:
        """
        Creates a delivery and returns True if it was created.
        :param post_id:
        :param city_id:
        :param address_id:
        :return:
        """
        try:
            delivery = Delivery(
                post_id=post_id,
                city_id=city_id,
                address_id=address_id
            )
            self.session.add(delivery)
            await self.session.commit()
            return delivery
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return False

    async def get_delivery(self, idx: int) -> dict | None:
        """
        Gets a delivery and returns it if it was created.
        :param idx:
        :return:
        """
        try:
            query = (select(
                Delivery,
                Post.name.label("name"),
                City.name.label("city"),
                Address.name.label("address"))
                     .join(Post, Delivery.post_id == Post.id)
                     .join(City, Delivery.city_id == City.id)
                     .join(Address, Delivery.address_id == Address.id)
                     .where(Delivery.id == idx))
            result = await self.session.execute(query)
            rows = result.one_or_none()
            if not rows:
                return None
            delivery, post_name, city_name, address_name = rows
            return {
                "delivery_id": delivery.id,
                "post_name": post_name,
                "city_name": city_name,
                "address_name": address_name
            }

        except Exception as e:
            logging.exception(e)
            return None

    async def update_delivery(self, idx: int,
                              post_id: int,
                              city_id: int,
                              address_id: int
                              ) -> bool:
        try:
            query = select(Delivery).where(Delivery.id == idx)
            result = await self.session.execute(query)
            delivery = result.scalar_one_or_none()
            if delivery is None:
                return False
            delivery.post_id = int(post_id)
            delivery.city_id = int(city_id)
            delivery.address_id = int(address_id)
            await self.session.commit()
            return True
        except Exception as e:
            logging.exception(e)
            return False

    async def get_deliveries(self) -> list | None:
        """
        Gets all deliveries and returns them if they were created.
        :return:
        """
        try:
            query = (select(
                Delivery,
                Post.name.label("name"),
                City.name.label("city"),
                Address.name.label("address"))
                     .join(Post, Delivery.post_id == Post.id)
                     .join(City, Delivery.city_id == City.id)
                     .join(Address, Delivery.address_id == Address.id))
            result = await self.session.execute(query)
            rows = result.all()
            if not rows:
                return None
            return [
                {
                    "delivery_id": delivery.id,
                    "post_name": post_name,
                    "city_name": city_name,
                    "address_name": address_name
                }
                for delivery, post_name, city_name, address_name in rows
            ]
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
