from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from html import escape
from database.main import Product
import logging
from typing import Sequence


class ProductManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_product(self, name: str, description: str,
                             amount: int, price: float) -> bool | Product:
        """
        Creates a new product.
        :param name:
        :param description:
        :param amount:
        :param price:
        :return:
        """
        try:
            name = escape(str(name))
            description = escape(str(description))
            amount = int(amount)
            price = float(price)
            product = Product(name=name, description=description,
                              amount=amount, price=price)
            self.session.add(product)
            await self.session.commit()
            return product
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return False

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
        except Exception as e:
            logging.exception(e)
            return None

    async def update_product(self, idx: int, name: str, description: str,
                             amount: int, price: float) -> bool:
        """
        Updates a product.
        :param idx:
        :param name:
        :param description:
        :param amount:
        :param price:
        :return:
        """
        try:
            query = select(Product).where(Product.id == idx)
            result = await self.session.execute(query)
            product = result.scalar_one_or_none()
            if product is None:
                return False

            product.name = name
            product.description = escape(str(description))
            product.amount = amount
            product.price = price

            await self.session.commit()
            return True
        except Exception as e:
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
            return result.scalars().all()
        except Exception as e:
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
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            return False
