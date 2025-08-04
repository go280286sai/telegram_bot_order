"""
Module for products database.
Includes operations for listing, creating, updating, and deleting products.
"""

from html import escape
import logging
from typing import Sequence
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from database.main import Review


class ReviewManager:
    """
    Class for managing products database.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_review(self,
                            name: str,
                            text_: str,
                            gender: int
                            ) -> None | Review:
        """
        Create a new review
        :param text_:
        :param name:
        :param gender:
        :return:
        """
        try:
            name = escape(str(name))
            text_ = escape(str(text_))
            gender = int(gender)
            if gender not in (0, 1):
                raise ValueError
            review_ = Review(name=name, text=text_, gender=gender)
            self.session.add(review_)
            await self.session.commit()
            return review_
        except ValueError as e:
            await self.session.rollback()
            logging.exception(e)
            return None

    async def update_review(self,
                            idx: int,
                            text_: str,
                            name: str,
                            gender: int
                            ) -> bool:
        """
        Update a review
        :param idx:
        :param text_:
        :param name:
        :param gender:
        :return:
        """
        try:
            if gender not in (0, 1):
                raise ValueError
            query = select(Review).where(Review.id == int(idx))
            result = await self.session.execute(query)
            review = result.scalar_one_or_none()
            if review is None:
                return False
            review.text = escape(str(text_))
            review.name = escape(str(name))
            review.gender = int(gender)
            await self.session.commit()
            return True
        except ValueError as e:
            logging.exception(e)
            return False

    async def get_reviews(self) -> Sequence[Review] | None:
        """
        Gets all reviews.
        :return:
        """
        try:
            query = select(Review)
            result = await self.session.execute(query)
            reviews_ = result.scalars().all()
            if reviews_ is None:
                return None
            return reviews_
        except ValueError as e:
            logging.exception(e)
            return None

    async def delete_review(self, idx: int) -> bool:
        """
        Deletes a review.
        :param idx:
        :return:
        """
        try:
            query = select(Review).where(Review.id == idx)
            result = await self.session.execute(query)
            review = result.scalar_one_or_none()
            if review is None:
                return False
            await self.session.delete(review)
            await self.session.commit()
            return True
        except ValueError as e:
            await self.session.rollback()
            logging.exception(e)
            return False

    async def truncate_reviews_table(self) -> bool:
        """
        Truncate the reviews table
        """
        try:
            await self.session.execute(text("DELETE FROM reviews"))
            await self.session.commit()
            return True
        except ValueError as e:
            await self.session.rollback()
            logging.exception(e)
            return False
