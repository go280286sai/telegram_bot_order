from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.main import Subscriber
import logging
from html import escape
from helps.helper import generate_transaction
from sqlalchemy import text


class SubscriberManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_subscriber(self,
                                email: str,
                                hash_active: str
                                ) -> None | Subscriber:
        """
        Create a new subscriber.
        :param email:
        :param hash_active:
        :return:
        """
        try:
            email = escape(email)
            sub = Subscriber(email=email, hashed_active=hash_active)
            self.session.add(sub)
            await self.session.commit()
            return sub
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return None

    async def set_active_subscriber(self, idx: int, hash_active: str) -> bool:
        """
        Set active subscriber.
        :param idx:
        :param hash_active:
        :return:
        """
        try:
            if idx <= 0:
                return False
            idx = int(idx)
            hash_active = escape(hash_active)
            query = select(Subscriber).where(Subscriber.id == idx)
            result = await self.session.execute(query)
            sub = result.scalar_one_or_none()
            if sub is None:
                return False
            if sub.hashed_active == hash_active:
                sub.status = 1
                sub.hashed_active = ""
                sub.hashed_destroy = generate_transaction()
                await self.session.commit()
                return True
            return False
        except Exception as e:
            logging.exception(e)
            return False

    async def set_destroy_subscriber(self,
                                     idx: int,
                                     hash_destroy: str
                                     ) -> bool:
        """
        Delete subscriber.
        :param idx:
        :param hash_destroy:
        :return:
        """
        try:
            if idx <= 0:
                return False
            idx = int(idx)
            query = select(Subscriber).where(Subscriber.id == idx)
            result = await self.session.execute(query)
            sub = result.scalar_one_or_none()
            if sub is None:
                return False
            if sub.hashed_destroy == hash_destroy:
                await self.session.delete(sub)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            logging.exception(e)
            return False

    async def get_subscribers(self) -> list | None:
        """
        Get subscribers.
        :return:
        """
        try:
            query = select(Subscriber)
            result = await self.session.execute(query)
            sub = result.scalars().all()
            if sub is None:
                return None
            subscribers_ = [
                {
                    "id": p.id,
                    "email": p.email,
                    "status": p.status,
                    "created_at": p.created_at.strftime("%Y-%m-%d")
                } for p in sub
            ]
            return subscribers_
        except Exception as e:
            logging.exception(e)
            return None

    async def get_active_subscribers(self) -> list | None:
        """
        Get subscribers.
        :return:
        """
        try:
            query = select(Subscriber).where(Subscriber.status == 1)
            result = await self.session.execute(query)
            sub = result.scalars().all()
            if sub is None:
                return None
            subscribers_ = [
                {
                    "id": p.id,
                    "email": p.email,
                    "status": p.status,
                    "created_at": p.created_at.strftime("%Y-%m-%d")
                } for p in sub
            ]
            return subscribers_
        except Exception as e:
            logging.exception(e)
            return None

    async def get_hashed_destroy(self,
                                 idx: int
                                 ) -> str | None:
        """
        Get hashed destroy.
        :return:
        """
        try:
            idx = int(idx)
            query = select(Subscriber).where(Subscriber.id == idx)
            result = await self.session.execute(query)
            sub = result.scalar_one_or_none()
            print(sub)
            if sub is None:
                return None
            return str(sub.hashed_destroy)
        except Exception as e:
            logging.exception(e)
            return None

    async def delete_subscriber(self, idx: int) -> bool:
        """
        Delete subscriber.
        :param idx:
        :return:
        """
        try:
            idx = int(idx)
            query = select(Subscriber).where(Subscriber.id == idx)
            result = await self.session.execute(query)
            sub = result.scalar_one_or_none()
            if sub is None:
                return False
            await self.session.delete(sub)
            await self.session.commit()
            return True
        except Exception as e:
            logging.exception(e)
            return False

    async def truncate_subscribers_table(self) -> bool:
        """
        Truncate the subscribers table
        """
        try:
            await self.session.execute(text("DELETE FROM subscribers"))
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return False
