from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.main import Setting
import logging
from typing import Sequence
from html import escape


class SettingManager:
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
            setting_ = Setting(name=name, value=value)
            self.session.add(setting_)
            await self.session.commit()
            return setting_
        except Exception as e:
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
            query = select(Setting).where(Setting.id == idx)
            result = await self.session.execute(query)
            setting_ = result.scalar_one_or_none()
            if setting_ is None:
                return None
            return setting_
        except Exception as e:
            logging.exception(e)
            return None

    async def update_setting(self,
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
            query = select(Setting).where(Setting.id == idx)
            result = await self.session.execute(query)
            setting_ = result.scalar_one_or_none()
            if setting_ is None:
                return False
            setting_.name = escape(str(name))
            setting_.value = escape(str(value))
            await self.session.commit()
            return True
        except Exception as e:
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
        except Exception as e:
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
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return False
