from typing import Tuple, Sequence

from sqlalchemy import Row
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from html import escape
from database.main import User, get_db
from helps.help import hash_password
import logging

logging.basicConfig(level=logging.INFO)


class UserManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, username: str, password: str, phone: str) -> bool:
        try:
            username = escape(username)
            password = hash_password(escape(password))
            phone = escape(phone)
            user = User(username=username, password=password, phone=phone)
            self.session.add(user)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logging.error(e)
            return False

    async def set_status(self, user_id: int, status: str) -> bool:
        try:
            query = select(User).where(User.id == user_id)
            result = await self.session.execute(query)
            user = result.scalar()
            user.status = status
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logging.error(e)
            return False

    async def add_comments(self, user_id: int, comments: str) -> bool:
        try:
            query = select(User).where(User.id == user_id)
            result = await self.session.execute(query)
            user = result.scalar()
            comments = escape(comments)
            user.comments = comments
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logging.error(e)
            return False

    async def reset_password(self, user_id: int) -> bool:
        try:
            query = select(User).where(User.id == user_id)
            result = await self.session.execute(query)
            user = result.scalar()
            user.password = hash_password("0000")
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logging.error(e)
            return False

    async def get_user(self, id: int) -> User | None:
        try:
            query = select(User).where(User.id == id)
            result = await self.session.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            logging.error(e)
            return None

    async def get_users(self) -> Sequence[User] | None:
        try:
            query = select(User)
            result = await self.session.execute(query)
            return result.scalars().all()
        except Exception as e:
            logging.error(e)
            return None

    async def delete_user(self, id: int) -> bool:
        try:
            query = select(User).where(User.id == id)
            result = await self.session.execute(query)
            user = result.scalar_one_or_none()  # Get the actual user object

            if user:
                await self.session.delete(user)
                await self.session.commit()
                return True

            return False  # User not found
        except Exception as e:
            await self.session.rollback()  # Ensure rollback on failure
            logging.error(e)
            return False
