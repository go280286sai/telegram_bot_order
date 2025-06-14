from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from html import escape
from database.main import Product
import logging
from typing import Sequence

logging.basicConfig(level=logging.INFO)


class ProductManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_product(self, name: str, description: str, amount: int, price: float) -> bool:
        try:
            name = escape(str(name))
            description = escape(str(description))
            amount = int(amount)
            price = float(price)
            product = Product(name=name, description=description, amount=amount, price=price)
            self.session.add(product)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logging.error(e)
            return False

    async def get_product(self, id: str) -> Product | None:
        try:
            query = select(Product).where(Product.id == id)
            result = await self.session.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            logging.error(e)
            return None

    async def update_product(self, id: int, name: str, description: str, amount: int, price: float) -> bool:
        try:
            query = select(Product).where(Product.id == id)
            result = await self.session.execute(query)
            product = result.scalar()
            product.name = name
            product.description = escape(str(description))
            product.amount = int(amount)
            product.price = float(price)
            await self.session.commit()
            return True
        except Exception as e:
            logging.error(e)
            return None

    async def get_products(self) -> Sequence[Product] | None:
        try:
            query = select(Product)
            result = await self.session.execute(query)
            return result.scalars().all()
        except Exception as e:
            logging.error(e)
            return None

    async def delete_product(self, id: str) -> bool:
        try:
            query = select(Product).where(Product.id == id)
            result = await self.session.execute(query)
            product = result.scalar_one_or_none()  # Get the actual user object

            if product:
                await self.session.delete(product)
                await self.session.commit()
                return True

            return False  # User not found
        except Exception as e:
            await self.session.rollback()  # Ensure rollback on failure
            logging.error(e)
            return False
