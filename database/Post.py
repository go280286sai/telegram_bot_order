from sqlalchemy import Row
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.main import Post
import logging
from typing import Sequence, Any
from html import escape


class PostManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_post(self, name: str) -> bool:
        """
        Creates a new post.
        :param name:
        :return:
        """
        try:
            post_ = Post(name=name)
            self.session.add(post_)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return False

    async def get_post(self, idx: int) -> Row[Any] | None:
        """
        Gets a post.
        :param idx:
        :return:
        """
        try:
            query = select(Post).where(Post.id == idx)
            result = await self.session.execute(query)
            post_ = result.scalar_one_or_none()
            if post_ is None:
                return None
            return post_
        except Exception as e:
            logging.exception(e)
            return None

    async def update_post(self,
                              idx: int,
                              name: str
                              ) -> bool:
        """
        Updates a post.
        :param idx:
        :param name:
        :return:
        """
        try:
            query = select(Post).where(Post.id == idx)
            result = await self.session.execute(query)
            post_ = result.scalar_one_or_none()
            if post_ is None:
                return False
            post_.name = escape(str(name))
            await self.session.commit()
            return True
        except Exception as e:
            logging.exception(e)
            return False

    async def get_posts(self) -> Sequence[Post] | None:
        """
        Gets all posts.
        :return:
        """
        try:
            query = select(Post)
            result = await self.session.execute(query)
            return result.scalars().all()
        except Exception as e:
            logging.exception(e)
            return None

    async def delete_post(self, idx: int) -> bool:
        """
        Deletes a post.
        :param idx:
        :return:
        """
        try:
            query = select(Post).where(Post.id == idx)
            result = await self.session.execute(query)
            post_ = result.scalar_one_or_none()
            if post_ is None:
                return False
            await self.session.delete(post_)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return False
