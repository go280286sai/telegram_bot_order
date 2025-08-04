"""
Module for user database.
Includes operations for listing, creating, updating, and deleting user.
"""

import logging
from html import escape
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from database.main import User
from helps.helper import hash_password, generate_transaction


class UserManager:
    """
    Class for managing user database.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(
        self,
            username: str,
            password: str,
            phone: str,
            email: str,
            hash_active_: str
    ) -> None | dict[str, str]:
        """
        Create a new user
        :param username:
        :param password:
        :param phone:
        :param email:
        :param hash_active_:
        :return:
        """
        try:
            users = select(User)
            users_result = await self.session.execute(users)
            results = users_result.scalars().all()
            is_admin = 1 if len(results) == 0 else 0
            username = escape(username)
            password = hash_password(escape(password))
            phone = escape(phone)
            email = escape(email)
            hash_active = hash_active_
            user = User(
                username=username,
                password=password,
                phone=phone,
                email=email,
                hashed_active=hash_active,
                is_admin=is_admin,
            )
            self.session.add(user)
            await self.session.commit()
            new_user = {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "is_admin": str(user.is_admin),
                "status": str(user.status),
                "hashed_active": user.hashed_active,
            }
            return new_user
        except ValueError as e:
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
        except ValueError as e:
            await self.session.rollback()
            logging.exception(e)
            return False

    async def update_user_name(
        self, idx: int, first_name: str, last_name: str
    ) -> bool | User:
        """
        Update a user
        :param last_name:
        :param first_name:
        :param idx:
        :return:
        """
        try:
            query = select(User).where(User.id == idx)
            result = await self.session.execute(query)
            user = result.scalar_one_or_none()
            if user is None:
                return False
            user.first_name = escape(first_name)
            user.last_name = escape(last_name)
            await self.session.commit()
            return user
        except ValueError as e:
            await self.session.rollback()
            logging.exception(e)
            return False

    async def update_users(
        self,
        idx: int,
        username: str,
        email: str,
        phone: str,
        comments: str,
        first_name: str,
        last_name: str,
    ) -> bool:
        """
        Update a user
        :param last_name:
        :param first_name:
        :param idx:
        :param username:
        :param email:
        :param phone:
        :param comments:
        :return:
        """
        try:
            query = select(User).where(User.id == idx)
            result = await self.session.execute(query)
            user = result.scalar_one_or_none()
            if user is None:
                return False
            user.username = escape(username)
            user.email = escape(email)
            user.phone = escape(phone)
            user.comments = escape(comments)
            user.first_name = escape(first_name)
            user.last_name = escape(last_name)
            await self.session.commit()
            return True
        except ValueError as e:
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
        except ValueError as e:
            await self.session.rollback()
            logging.exception(e)
            return False

    async def set_admin(self, user_id: int, status: int) -> bool:
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
            user.is_admin = status
            await self.session.commit()
            return True
        except ValueError as e:
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
        except ValueError as e:
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
        except ValueError as e:
            await self.session.rollback()
            logging.exception(e)
            return None

    async def get_user(self, idx: int) -> None | dict:
        """
        Get a user
        :param idx:
        :return:
        """
        try:
            query = select(User).where(User.id == int(idx))
            result = await self.session.execute(query)
            user = result.scalar_one_or_none()
            if user is None:
                return None
            user_ = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "status": user.status,
                "comments": user.comments,
                "is_admin": user.is_admin,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "bonus": user.bonus,
                "hashed_active": user.hashed_active,
                "created_at": user.created_at.strftime("%Y-%m-%d"),
            }

            return user_
        except ValueError as e:
            logging.exception(e)
            return None

    async def get_users(self) -> list | None:
        """
        Get all users
        :return:
        """
        try:
            query = select(User)
            result = await self.session.execute(query)
            users = result.scalars().all()
            if users is None:
                return None
            users_ = [
                {
                    "id": p.id,
                    "username": p.username,
                    "email": p.email,
                    "phone": p.phone,
                    "status": p.status,
                    "comments": p.comments,
                    "is_admin": p.is_admin,
                    "first_name": p.first_name,
                    "last_name": p.last_name,
                    "bonus": p.bonus,
                    "created_at": p.created_at.strftime("%Y-%m-%d"),
                }
                for p in users
            ]
            return users_
        except ValueError as e:
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
        except ValueError as e:
            await self.session.rollback()
            logging.exception(e)
            return False

    async def get_user_by_username(self,
                                   username: str,
                                   password: str
                                   ) -> User | None:
        """
        Get a user
        :param username:
        :param password:
        :return:
        """
        try:
            username = escape(username)
            password = hash_password(escape(password))
            query = (
                select(User)
                .where(User.username == username)
                .where(User.password == password)
            )
            result = await self.session.execute(query)
            user = result.scalar_one_or_none()
            if user is None:
                return None
            return user
        except ValueError as e:
            logging.exception(e)
            return None

    async def get_user_by_username_email(
        self, username: str, email: str
    ) -> None | User:
        """
        Get a user
        :param username:
        :param email:
        :return:
        """
        try:
            username = escape(username)
            query = (
                select(User)
                .where(User.username == username)
                .where(User.email == email)
            )
            result = await self.session.execute(query)
            user = result.scalar_one_or_none()
            if user is None:
                return None
            return user
        except ValueError as e:
            logging.exception(e)
            return None

    async def set_hashed_active_for_delete(
        self, idx: str, hashed_active: str
    ) -> None | str:
        """
        Set a hashed active for delete
        :param hashed_active:
        :param idx:
        :return:
        """
        try:
            query = select(User).where(User.id == int(idx))
            result = await self.session.execute(query)
            user = result.scalar_one_or_none()
            if user is None:
                return None
            user.hashed_active = hashed_active
            await self.session.commit()
            return user.email
        except ValueError as e:
            logging.exception(e)
            return None

    async def truncate_users_table(self) -> bool:
        """
        Truncate the users table
        """
        try:
            await self.session.execute(text("DELETE FROM users"))
            await self.session.commit()
            return True
        except ValueError as e:
            await self.session.rollback()
            logging.exception(e)
            return False

    async def bonus(self, idx: int, target: str, total: int) -> bool:
        """
        Add a bonus to a user
        :param total:
        :param target:
        :param idx:
        :return:
        """
        try:
            query = select(User).where(User.id == int(idx))
            result = await self.session.execute(query)
            user = result.scalar_one_or_none()
            if user is None:
                return False
            if target == "add":
                user.bonus += total
            elif target == "remove":
                user.bonus -= total
            await self.session.commit()
            return True
        except ValueError as e:
            logging.exception(e)
            return False
