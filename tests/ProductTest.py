import sys

sys.path.append("D:/dev/python/projects/bot_order")

import pytest
from database.Products import ProductManager
from database.main import async_session_maker
from helps.help import hash_password

@pytest.mark.asyncio
async def test_create_product():
    async with async_session_maker() as session:
        product_manager = ProductManager(session)
        product = await product_manager.create_product("Product", "This product is a test", amount=10, price=10.50)
        assert product == True

@pytest.mark.asyncio
async def test_update_product():
    async with async_session_maker() as session:
        product_manager = ProductManager(session)
        query = await product_manager.update_product(1, "ProductNew", "This product is a test 2", amount=20, price=12.80)
        assert query is True


@pytest.mark.asyncio
async def test_get_product():
    async with async_session_maker() as session:
        product_manager = ProductManager(session)
        query = await product_manager.get_product(1)
        assert query.name == "ProductNew"
        assert query.description == "This product is a test 2"
        assert query.amount == 20
        assert query.price == 12.80



@pytest.mark.asyncio
async def test_get_products():
    async with async_session_maker() as session:
        product_manager = ProductManager(session)
        products = await product_manager.get_products()
        for product in products:
            assert product.name == "ProductNew"
            assert product.description == "This product is a test 2"
            assert product.amount == 20
            assert product.price == 12.80

@pytest.mark.asyncio
async def test_delete_product():
    async with async_session_maker() as session:
        product_manager = ProductManager(session)
        query = await product_manager.delete_product(1)
        assert query is True
