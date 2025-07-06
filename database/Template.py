from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.main import Temlate
import logging
from typing import Sequence
from html import escape


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
            email = Temlate(
                header=header,
                title=title,
                body=body
            )
            self.session.add(email)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return False

    async def get_template(self, idx: int) -> Temlate | None:
        """
        Gets a template.
        :param idx:
        :return:
        """
        try:
            query = select(Temlate).where(Temlate.id == idx)
            result = await self.session.execute(query)
            email = result.scalar_one_or_none()
            if email is None:
                return None
            return email
        except Exception as e:
            logging.exception(e)
            return None

    async def get_templates(self) -> Sequence[Temlate] | None:
        """
        Gets all templates.
        :return:
        """
        try:
            query = select(Temlate)
            result = await self.session.execute(query)
            templates = result.scalars().all()
            if templates is None:
                return None
            return templates
        except Exception as e:
            logging.exception(e)
            return None

    async def update_template(self,
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
            query = select(Temlate).where(Temlate.id == idx)
            result = await self.session.execute(query)
            email = result.scalar_one_or_none()
            if email is None:
                return False
            email.header = escape(str(header))
            email.title = escape(str(title))
            email.body = escape(str(body))
            await self.session.commit()
            return True
        except Exception as e:
            logging.exception(e)
            return False

    async def delete_template(self, idx: int) -> bool:
        """
        Deletes a template.
        :param idx:
        :return:
        """
        try:
            query = select(Temlate).where(Temlate.id == idx)
            result = await self.session.execute(query)
            email = result.scalar_one_or_none()
            if email is None:
                return False
            await self.session.delete(email)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return False
