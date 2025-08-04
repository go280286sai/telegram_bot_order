"""
Module for template database.
Includes operations for listing, creating, updating, and deleting template.
"""

import logging
from typing import Sequence
from html import escape
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from database.main import Template


class TemplateManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_template(self,
                              header: str,
                              title: str,
                              body: str
                              ) -> bool:
        """
        Creates a new template for send emails.
        :param header:
        :param title:
        :param body:
        :return:
        """
        try:
            email = Template(header=header, title=title, body=body)
            self.session.add(email)
            await self.session.commit()
            return True
        except ValueError as e:
            await self.session.rollback()
            logging.exception(e)
            return False

    async def get_template(self, idx: int) -> Template | None:
        """
        Gets a template.
        :param idx:
        :return:
        """
        try:
            query = select(Template).where(Template.id == idx)
            result = await self.session.execute(query)
            tmp = result.scalar_one_or_none()
            if tmp is None:
                return None
            return tmp
        except ValueError as e:
            logging.exception(e)
            return None

    async def get_templates(self) -> Sequence[Template] | None:
        """
        Gets all templates.
        :return:
        """
        try:
            query = select(Template)
            result = await self.session.execute(query)
            templates = result.scalars().all()
            if templates is None:
                return None
            return templates
        except ValueError as e:
            logging.exception(e)
            return None

    async def update_template(
        self,
        idx: int,
        header: str,
        title: str,
        body: str,
    ) -> bool:
        """
        Updates a template.
        :param idx:
        :param header:
        :param title:
        :param body:
        :return:
        """
        try:
            if idx <= 0:
                return False
            query = select(Template).where(Template.id == idx)
            result = await self.session.execute(query)
            email = result.scalar_one_or_none()
            if email is None:
                return False
            email.header = escape(str(header))
            email.title = escape(str(title))
            email.body = escape(str(body))
            await self.session.commit()
            return True
        except ValueError as e:
            logging.exception(e)
            return False

    async def delete_template(self, idx: int) -> bool:
        """
        Deletes a template.
        :param idx:
        :return:
        """
        try:
            query = select(Template).where(Template.id == idx)
            result = await self.session.execute(query)
            email = result.scalar_one_or_none()
            if email is None:
                return False
            await self.session.delete(email)
            await self.session.commit()
            return True
        except ValueError as e:
            await self.session.rollback()
            logging.exception(e)
            return False

    async def truncate_templates_table(self) -> bool:
        """
        Truncate the template table
        """
        try:
            await self.session.execute(text("DELETE FROM templates"))
            await self.session.commit()
            return True
        except ValueError as e:
            await self.session.rollback()
            logging.exception(e)
            return False
