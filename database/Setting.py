"""
Module for setting database.
Includes operations for listing, creating, updating, and deleting setting.
"""

import logging
from typing import Sequence
from html import escape
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from database.main import Setting


class SettingManager:
    """
    Class for managing database settings.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_setting(self, name: str, value: str) -> Setting | None:
        """
        Creates a new setting.
        :param name:
        :param value:
        :return:
        """
        try:
            name = escape(name)
            value = escape(value)
            setting_ = Setting(name=name, value=value)
            self.session.add(setting_)
            await self.session.commit()
            return setting_
        except ValueError as e:
            await self.session.rollback()
            logging.exception(e)
            return None

    async def get_setting(self, idx: int) -> Setting | None:
        """
        Gets a setting.
        :param idx:
        :return:
        """
        try:
            query = select(Setting).where(Setting.id == int(idx))
            result = await self.session.execute(query)
            setting_ = result.scalar_one_or_none()
            if setting_ is None:
                return None
            return setting_
        except ValueError as e:
            logging.exception(e)
            return None

    async def update_setting(
        self,
        idx: int,
        name: str,
        value: str,
    ) -> bool:
        """
        Updates a setting.
        :param idx:
        :param name:
        :param value:
        :return:
        """
        try:
            name = escape(name)
            value = escape(value)
            query = select(Setting).where(Setting.id == int(idx))
            result = await self.session.execute(query)
            setting_ = result.scalar_one_or_none()
            if setting_ is None:
                return False
            setting_.name = escape(str(name))
            setting_.value = escape(str(value))
            await self.session.commit()
            return True
        except ValueError as e:
            logging.exception(e)
            return False

    async def get_settings(self) -> Sequence[Setting] | None:
        """
        Gets all settings.
        :return:
        """
        try:
            query = select(Setting)
            result = await self.session.execute(query)
            return result.scalars().all()
        except ValueError as e:
            logging.exception(e)
            return None

    async def delete_setting(self, idx: int) -> bool:
        """
        Deletes a setting.
        :param idx:
        :return:
        """
        try:
            query = select(Setting).where(Setting.id == idx)
            result = await self.session.execute(query)
            setting_ = result.scalar_one_or_none()
            if setting_ is None:
                return False
            await self.session.delete(setting_)
            await self.session.commit()
            return True
        except ValueError as e:
            await self.session.rollback()
            logging.exception(e)
            return False

    async def truncate_settings_table(self) -> bool:
        """
        Truncate the settings table
        """
        try:
            await self.session.execute(text("DELETE FROM settings"))
            await self.session.commit()
            return True
        except ValueError as e:
            await self.session.rollback()
            logging.exception(e)
            return False
