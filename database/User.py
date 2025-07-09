from typing import Sequence
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from html import escape
from database.main import User
from helps.help import hash_password, generate_transaction
import logging

RESET_PASSWORD = "0000"


class UserManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self,
                          username: str,
                          password: str,
                          phone: str,
                          email: str,
                          hash_active: str
                          ) -> None | User:
        """
        Create a new user
        :param username:
        :param password:
        :param phone:
        :param email:
        :param hash_active:
        :return:
        """
        try:
            username = escape(username)
            password = hash_password(escape(password))
            phone = escape(phone)
            email = escape(email)
            hash_active = hash_active
            user = User(username=username, password=password,
                        phone=phone, email=email, hashed_active=hash_active)
            self.session.add(user)
            await self.session.commit()
            return user
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return None

    async def update_user(self, idx: int, password: str) -> bool | User:
        """
        Update a user
        :param idx:
        :param password:
        :return:
        """
        try:
            query = select(User).where(User.id == idx)
            result = await self.session.execute(query)
            user = result.scalar_one_or_none()
            if user is None:
                return False
            user.password = hash_password(escape(password))
            await self.session.commit()
            return user
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return False

    async def set_status(self, user_id: int, status: int) -> bool:
        """
        Change status of a user
        :param user_id:
        :param status:
        :return:
        """
        try:
            query = select(User).where(User.id == user_id)
            result = await self.session.execute(query)
            user = result.scalar_one_or_none()
            if user is None:
                return False
            user.status = status
            user.hashed_active = ""
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return False

    async def add_comments(self, user_id: int, comments: str) -> bool:
        """
        Add comments to a user
        :param user_id:
        :param comments:
        :return:
        """
        try:
            query = select(User).where(User.id == user_id)
            result = await self.session.execute(query)
            user = result.scalar_one_or_none()
            if user is None:
                return False
            user.comments = escape(comments)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return False

    async def reset_password(self, user_id: int) -> None | str:
        """
        Reset password of a user
        :param user_id:
        :return:
        """
        try:
            query = select(User).where(User.id == user_id)
            result = await self.session.execute(query)
            user = result.scalar_one_or_none()
            if user is None:
                return None
            password = str(generate_transaction())
            user.password = hash_password(password)
            await self.session.commit()
            return password
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return None

    async def get_user(self, idx: int) -> User | None:
        """
        Get a user
        :param idx:
        :return:
        """
        try:
            query = select(User).where(User.id == idx)
            result = await self.session.execute(query)
            user = result.scalar_one_or_none()
            if user is None:
                return None
            return user
        except Exception as e:
            logging.exception(e)
            return None

    async def get_users(self) -> Sequence[User] | None:
        """
        Get all users
        :return:
        """
        try:
            query = select(User)
            result = await self.session.execute(query)
            return result.scalars().all()
        except Exception as e:
            logging.exception(e)
            return None

    async def delete_user(self, idx: int) -> bool:
        """
        Delete a user
        :param idx:
        :return:
        """
        try:
            query = select(User).where(User.id == idx)
            result = await self.session.execute(query)
            user = result.scalar_one_or_none()
            if user is None:
                return False
            await self.session.delete(user)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return False

    async def get_user_by_username(self, username: str,
                                   password: str) -> User | None:
        """
        Get a user
        :param username:
        :param password:
        :return:
        """
        try:
            username = escape(username)
            password = hash_password(escape(password))
            query = (select(User)
                     .where(User.username == username)
                     .where(User.password == password))
            result = await self.session.execute(query)
            user = result.scalar_one_or_none()
            if user is None:
                return None
            return user
        except Exception as e:
            logging.exception(e)
            return None

    async def get_user_by_username_email(self,
                                         username: str,
                                         email: str
                                         ) -> None | User:
        """
        Get a user
        :param username:
        :param email:
        :return:
        """
        try:
            username = escape(username)
            query = (select(User)
                     .where(User.username == username)
                     .where(User.email == email))
            result = await self.session.execute(query)
            user = result.scalar_one_or_none()
            if user is None:
                return None
            return user
        except Exception as e:
            logging.exception(e)
            return None
