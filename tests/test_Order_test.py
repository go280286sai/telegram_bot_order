import pytest

from database.Address import AddressManager
from database.City import CityManager
from database.Orders import OrderManager
from database.Post import PostManager
from database.Products import ProductManager
from database.User import UserManager
from database.main import async_session_maker, Product, User
from helps.help import generate_transaction


@pytest.mark.asyncio
async def test_create_order():
    async with async_session_maker() as session:
        post_manager = PostManager(session)
        await post_manager.create_post(name="Test Post")
        city_manager = CityManager(session)
        await city_manager.create_city(name="Test City", post_id=1)
        address_manager = AddressManager(session)
        await address_manager.create_address(name="Test Address", city_id=1)
        product_manager = ProductManager(session)
        product = await product_manager.create_product(
            name="Product",
            description="This product is a test",
            amount=10,
            price=10.50)
        assert isinstance(product, Product)
        order_manager = OrderManager(session)
        order = await order_manager.create_order(
            products="{'1':1}",
            user_id=1,
            delivery="{\"post_id\": 1, \"city_id\": 1, \"address\": 1}",
            total=500.00,
            transaction_id="123"
        )
        assert order is True
        user_manager = UserManager(session)
        user = await user_manager.create_user(
            username="Alex",
            password="0000",
            phone="0123456789",
            email="admin@admin.com",
            hash_active=generate_transaction()
        )
        assert isinstance(user, User)


@pytest.mark.asyncio
async def test_get_order():
    async with async_session_maker() as session:
        # User
        order_manager = OrderManager(session)
        query = await order_manager.get_order(1)
        assert query.user_id == 1
        assert query.products == "{'1':1}"
        assert query.delivery == ("{\"post_id\": 1, "
                                  "\"city_id\": 1,"
                                  " \"address\": 1}")
        assert query.status == 0
        assert query.invoice is None
        assert query.comment is None
        assert query.total == 500.00
        assert query.transaction_id == "123"
        assert query.user.username == "Alex"
        assert query.user.phone == "0123456789"


@pytest.mark.asyncio
async def test_set_status():
    async with async_session_maker() as session:
        order_manager = OrderManager(session)
        query = await order_manager.set_status(1, 1)
        assert query is True
        query = await order_manager.set_status(1, 3)
        assert query is False


@pytest.mark.asyncio
async def test_get_order_user():
    async with (async_session_maker() as session):
        # User
        order_manager = OrderManager(session)
        query = await order_manager.get_orders_user(1)
        for user in query:
            assert user['id'] == 1
            assert user['status'] == 1
            assert user['total'] == 500.00


@pytest.mark.asyncio
async def test_set_invoice():
    async with (async_session_maker() as session):
        # User
        order_manager = OrderManager(session)
        query = await order_manager.set_invoice_order(idx=1, invoice="123456")
        assert query is True


@pytest.mark.asyncio
async def test_add_comment():
    async with async_session_maker() as session:
        order_manager = OrderManager(session)
        query = await order_manager.add_comment(idx=1, comment="Comment")
        assert query is True


@pytest.mark.asyncio
async def test_get_orders():
    async with async_session_maker() as session:
        order_manager = OrderManager(session)
        orders = await order_manager.get_orders()
        for query in orders:
            assert query['user'] == 1
            assert query['products'] == "{'1':1}"
            assert query['delivery'] == ("{\"post_id\": 1,"
                                         " \"city_id\": 1,"
                                         " \"address\": 1}")
            assert query['status'] == 1
            assert query['invoice'] == "123456"
            assert query['comment'] == "Comment"
            assert query['total'] == 500.00
            assert query['transaction_id'] == "123"


@pytest.mark.asyncio
async def test_get_predict(monkeypatch):
    def mock_build(self, data):
        return True

    async with async_session_maker() as session:
        from database.Orders import Predict
        monkeypatch.setattr(Predict, "build", mock_build)
        order_manager = OrderManager(session)
        query = await order_manager.get_predict(9)
        assert query is True


@pytest.mark.asyncio
async def test_get_delivery():
    async with async_session_maker() as session:
        order_manager = OrderManager(session)
        query = await order_manager.get_delivery(
            post_id=1,
            city_id=1,
            address_id=1
        )
        assert query['post_name'] == "Test Post"
        assert query['city_name'] == "Test City"
        assert query['address_name'] == "Test Address"


@pytest.mark.asyncio
async def test_delete_order():
    async with async_session_maker() as session:
        order_manager = OrderManager(session)
        query = await order_manager.delete_order(1)
        assert query is True
        query = await order_manager.delete_order(1)
        assert query is False

        product_manager = ProductManager(session)
        result = await product_manager.delete_product(1)
        assert result is True

        address_manager = AddressManager(session)
        result = await address_manager.delete_address(1)
        assert result is True

        city_manager = CityManager(session)
        result = await city_manager.delete_city(1)
        assert result is True

        post_manager = PostManager(session)
        result = await post_manager.delete_post(1)
        assert result is True

        user_manager = UserManager(session)
        await user_manager.delete_user(1)


@pytest.mark.asyncio
async def test_truncate_orders():
    async with async_session_maker() as session:
        user_manager = OrderManager(session)
        query = await user_manager.truncate_orders_table()
        assert query is True
