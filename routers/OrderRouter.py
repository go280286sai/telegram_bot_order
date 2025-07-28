import json
import logging
import re
from datetime import datetime

from database.Products import ProductManager
from database.User import UserManager
from helps.Middleware import is_admin
from helps.emails import send_emails
from helps.help import generate_transaction
from fastapi import APIRouter, Request, status, Response
from starlette.responses import JSONResponse
from database.Orders import OrderManager
from database.main import async_session_maker
from models.CommentModel import Comment
from models.InvoiceModal import Invoice
from models.PayModel import Pay
from models.TransactionModel import Transaction

router = APIRouter()


@router.post("/create")
async def create_order(
        transact: Transaction,
        request: Request,
        response: Response
):
    try:
        transaction = transact.transaction

        if transaction is None:
            raise Exception("Transaction cannot be None")
        user = request.cookies.get('user_id')
        if user is None:
            raise Exception("User does not exist")
        products = request.cookies.get('cart')
        if not products:
            raise Exception("No products")
        delivery = request.cookies.get('delivery')
        if not delivery:
            raise Exception("No delivery")
        total_price = transact.cardTotal
        if not total_price or total_price == 0:
            raise Exception("No total price")
        pay_bonus = request.cookies.get('bonus', 0)
        pay_discount = request.cookies.get('discount', 0)
        async with async_session_maker() as session:
            order_manager = OrderManager(session)
            await order_manager.create_order(
                products=products,
                user_id=int(user),
                delivery=json.dumps(delivery),
                total=float(total_price),
                transaction_id=transaction,
                bonus=int(pay_bonus),
                discount=int(pay_discount)
            )
            user_manager = UserManager(session)
            await user_manager.bonus(
                idx=int(user),
                target="add",
                total=int(total_price*2/100))

            if pay_bonus:
                await user_manager.bonus(
                    idx=int(user),
                    target="remove",
                    total=int(pay_bonus))

            response.delete_cookie("cart")
            return {
                "success": True,
                "data": None,
                "error": None
            }

    except Exception as e:
        logging.exception(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": str(e)
            }
        )


@router.post("/get_orders_user")
async def get_orders_user(request: Request) -> JSONResponse:
    """
    Get orders user
    :param request:
    :return:
    """
    try:
        async with async_session_maker() as session:
            user_id = request.cookies.get("user_id")
            if user_id is None:
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={"success": True, "data": None, "error": None}
                )
            order_manager = OrderManager(session)
            orders = await order_manager.get_orders_user(int(user_id))
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": {"orders": orders},
                    "error": None
                }
            )

    except Exception as e:
        logging.exception(f"get_orders_user failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed to fetch orders"
            }
        )


@router.post("/pay")
async def pay(pay_: Pay):
    try:
        pay_total = pay_.cardTotal
        if pay_total <= 0:
            raise Exception("Total is zero")
        clean_number = pay_.cardNumber.replace(" ", "")
        if not re.fullmatch(r"\d{16}", clean_number):
            raise Exception("Invalid card number")
        month = int(pay_.cardMonth)
        if not (1 <= month <= 12):
            raise Exception("Invalid expiry month")
        year = int("20" + pay_.cardYear)
        current_year = int(datetime.now().strftime("%Y"))
        if year < current_year:
            raise Exception("Invalid data year")
        if not re.fullmatch(r"\d{3,4}", pay_.cardKey):
            raise Exception("Invalid CVV")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "data": {"transaction_id": generate_transaction()},
                "error": None
            }
        )
    except Exception as e:
        logging.exception(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": str(e)
            }
        )


@router.post("/gets")
async def get_orders(request: Request) -> JSONResponse:
    """
    Get orders user
    :param request:
    :return:
    """
    try:
        user_id = request.cookies.get("user_id")
        if user_id is None:
            raise Exception("Cookies missing user_id")
        admin = await is_admin(int(user_id))
        if admin is None or admin is False:
            raise Exception("Cookies missing user_id")
        async with async_session_maker() as session:
            order_manager = OrderManager(session)
            orders = await order_manager.get_orders()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": {"orders": orders},
                    "error": None
                }
            )

    except Exception as e:
        logging.exception(f"get_orders_user failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed to fetch orders"
            }
        )


@router.post("/send_invoice/{idx}/{order_id}")
async def send_invoice(
        idx: int,
        order_id: int,
        invoice: Invoice,
        request: Request
) -> JSONResponse:
    """
    Send invoice
    :param order_id:
    :param idx:
    :param invoice:
    :param request:
    :return:
    """
    try:
        user_id = request.cookies.get("user_id")
        if user_id is None:
            raise Exception("Cookies missing user_id")
        admin = await is_admin(int(user_id))
        if admin is None or admin is False:
            raise Exception("Cookies missing user_id")
        async with async_session_maker() as session:
            order_manager = OrderManager(session)
            orders = await order_manager.set_invoice_order(
                idx=int(order_id),
                invoice=invoice.body,
            )
            if orders is False:
                raise Exception("Invoice order failed")
            user_manager = UserManager(session)
            user = await user_manager.get_user(int(idx))
            if user is None:
                raise Exception("Fetch user failed")
            await send_emails(
                header="Send invoice",
                title="Invoice",
                body=f"Your invoice: {invoice.body}",
                idx=int(idx),
                email=user.email,
                hash_active="",
                footer=False
            )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": None,
                    "error": None
                }
            )

    except Exception as e:
        logging.exception(f"Invoice order failed: {e}")
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "data": None,
                "error": "Invoice order failed"
            }
        )


@router.post("/add_comment/{idx}")
async def add_comment(
        idx: int,
        comment: Comment,
        request: Request
) -> JSONResponse:
    """
    Add comment
    :param comment:
    :param idx:
    :param request:
    :return:
    """
    try:
        user_id = request.cookies.get("user_id")
        if user_id is None:
            raise Exception("Cookies missing user_id")
        admin = await is_admin(int(user_id))
        if admin is None or admin is False:
            raise Exception("Cookies missing user_id")
        async with async_session_maker() as session:
            order_manager = OrderManager(session)
            orders = await order_manager.add_comment(
                idx=int(idx),
                comment=comment.body,
            )
            if orders is False:
                raise Exception("Invoice order failed")
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": None,
                    "error": None
                }
            )

    except Exception as e:
        logging.exception(f"Comment order failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Comment order failed"
            }
        )


@router.post("/get_view/{idx}")
async def get_order_view(idx: int, request: Request):
    """
    Get view
    :param idx:
    :param request:
    :return:
    """
    try:
        user_id = request.cookies.get("user_id")
        if user_id is None:
            raise Exception("Cookies missing user_id")
        admin = await is_admin(int(user_id))
        if admin is None or admin is False:
            raise Exception("Cookies missing user_id")
        async with async_session_maker() as session:
            order_manager = OrderManager(session)
            orders = await order_manager.get_order(idx=int(idx))
            if not orders:
                raise Exception("Invoice order failed")
            id = orders.id
            products = json.loads(orders.products)
            products_ = []
            product_manager = ProductManager(session)
            for product_id, amount in products.items():
                product = await product_manager.get_product(product_id)
                if product:
                    product_data = product.to_dict() if hasattr(
                        product, "to_dict") else {
                        "id": product.id,
                        "name": product.name,
                        "price": product.price,
                        "description": product.description,
                        "amounts": product.amount,
                    }
                    product_data["amount"] = amount
                    products_.append(product_data)

            delivery = orders.delivery

            if not delivery:
                raise Exception("No delivery")
            obj = json.loads(delivery)
            delivery = json.loads(obj)

            delivery_manager = OrderManager(session)

            delivery_query = await delivery_manager.get_delivery(
                post_id=int(delivery["post_id"]),
                city_id=int(delivery["city_id"]),
                address_id=int(delivery["address"])
            )

            user_ = {
                "first_name": orders.user.first_name,
                "last_name": orders.user.last_name,
                "phone": orders.user.phone,
                "email": orders.user.email
            }

            data = {
                "id": id,
                "delivery": delivery_query,
                "user": user_,
                "total": orders.total,
                "created": orders.created_at.strftime("%d-%m-%Y"),
                "invoice": orders.invoice,
                "products": products_,
                "bonus": orders.bonus,
                "discount": orders.discount
            }

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": data,
                    "error": None
                }
            )

    except Exception as e:
        logging.exception(f"Comment order failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": str(e)
            }
        )


@router.post("/get_predict/{n}")
async def get_predict(n: int, request: Request) -> JSONResponse:
    try:
        user_id = request.cookies.get("user_id")
        if user_id is None:
            raise Exception("Cookies missing user_id")
        admin = await is_admin(int(user_id))
        if admin is None or admin is False:
            raise Exception("Cookies missing user_id")
        async with async_session_maker() as session:
            order_manager = OrderManager(session)
            orders = await order_manager.get_predict(term=int(n))
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": {"predict": orders},
                    "error": None
                }
            )

    except Exception as e:
        logging.exception(f"get_orders_user failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed to fetch orders"
            }
        )


@router.post("/delete/{idx}")
async def delete(idx: int, request: Request) -> JSONResponse:
    """
    Delete order
    :param idx:
    :param request:
    :return:
    """
    try:
        user_id = request.cookies.get("user_id")
        if user_id is None:
            raise Exception("Cookies missing user_id")
        admin = await is_admin(int(user_id))
        if admin is None or admin is False:
            raise Exception("Cookies missing user_id")
        async with async_session_maker() as session:
            order_manager = OrderManager(session)
            orders = await order_manager.delete_order(
                idx=int(idx)
            )
            if orders is False:
                raise Exception("Delete order failed")
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": None,
                    "error": None
                }
            )

    except Exception as e:
        logging.exception(f"Delete order failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": str(e)
            }
        )
