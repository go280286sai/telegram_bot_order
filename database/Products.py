"""
Module for products database.
Includes operations for listing, creating, updating,
and deleting products.
"""

from html import escape
import logging
from typing import Sequence
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from database.main import Product


class ProductManager:
    """
    Class for managing products.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_product(
        self, name: str, description: str, amount: int, price: float
    ) -> None | Product:
        """
        Creates a new product.
        :param name:
        :param description:
        :param amount:
        :param price:
        :return:
        """
        try:
            if amount < 0 or price < 0:
                return None
            name = escape(str(name))
            description = escape(str(description))
            amount = int(amount)
            price = float(price)
            product = Product(
                name=name, description=description, amount=amount, price=price
            )
            self.session.add(product)
            await self.session.commit()
            return product
        except ValueError as e:
            await self.session.rollback()
            logging.exception(e)
            return None

    async def get_product(self, idx: int) -> Product | None:
        """
        Gets a product.
        :param idx:
        :return:
        """
        try:
            query = select(Product).where(Product.id == idx)
            result = await self.session.execute(query)
            product = result.scalar_one_or_none()
            if product is None:
                return None
            return product
        except ValueError as e:
            logging.exception(e)
            return None

    async def update_product(
        self,
        idx: int,
        name: str,
        description: str,
        amount: int,
        price: float,
        service: int,
    ) -> bool:
        """
        Updates a product.
        :param idx:
        :param name:
        :param description:
        :param amount:
        :param price:
        :param service:
        :return:
        """
        try:
            if amount < 0 or price < 0:
                raise ValueError
            query = select(Product).where(Product.id == int(idx))
            result = await self.session.execute(query)
            product = result.scalar_one_or_none()
            if product is None:
                return False

            product.name = name
            product.description = escape(str(description))
            product.amount = amount
            product.price = price
            product.service = service

            await self.session.commit()
            return True
        except ValueError as e:
            logging.exception(e)
            return False

    async def set_amount_product(self, idx: int, amount: int) -> bool:
        """
        Set amount a product.
        :param amount:
        :param idx:
        :return:
        """
        try:
            if amount <= 0:
                return False
            query = select(Product).where(Product.id == int(idx))
            result = await self.session.execute(query)
            product = result.scalar_one_or_none()
            if product is None:
                return False
            product.amount -= amount

            await self.session.commit()
            return True
        except ValueError as e:
            logging.exception(e)
            return False

    async def get_products(self) -> Sequence[Product] | None:
        """
        Gets all products.
        :return:
        """
        try:
            query = select(Product)
            result = await self.session.execute(query)
            products = result.scalars().all()
            if products is None:
                return None
            return products
        except ValueError as e:
            logging.exception(e)
            return None

    async def delete_product(self, idx: int) -> bool:
        """
        Deletes a product.
        :param idx:
        :return:
        """
        try:
            query = select(Product).where(Product.id == idx)
            result = await self.session.execute(query)
            product = result.scalar_one_or_none()
            if product is None:
                return False
            await self.session.delete(product)
            await self.session.commit()
            return True
        except ValueError as e:
            await self.session.rollback()
            logging.exception(e)
            return False

    async def truncate_products_table(self) -> bool:
        """
        Truncate the products table
        """
        try:
            await self.session.execute(text("DELETE FROM products"))
            await self.session.commit()
            return True
        except ValueError as e:
            await self.session.rollback()
            logging.exception(e)
            return False
