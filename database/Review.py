from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from html import escape
from database.main import Review
import logging
from typing import Sequence
from sqlalchemy import text


class ReviewManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_review(self, name: str, text: str,
                            gender: int) -> None | Review:
        """
        Create a new review
        :param text:
        :param name:
        :param gender:
        :return:
        """
        try:
            name = escape(str(name))
            text = escape(str(text))
            gender = int(gender)
            if gender not in (0, 1):
                raise ValueError
            review_ = Review(name=name, text=text, gender=gender)
            self.session.add(review_)
            await self.session.commit()
            return review_
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return None

    async def update_review(
            self, idx: int,
            text: str,
            name: str,
            gender: int
    ) -> bool:
        """
        Update a review
        :param idx:
        :param text:
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
            review.text = escape(str(text))
            review.name = escape(str(name))
            review.gender = int(gender)
            await self.session.commit()
            return True
        except Exception as e:
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
        except Exception as e:
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
        except Exception as e:
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
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return False
