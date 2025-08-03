"""
Router module for managing user orders-related endpoints.
Includes operations for listing, creating, updating, and deleting order.
"""
import json
import logging
import re
from datetime import datetime
from fastapi import APIRouter, Request, status, HTTPException, BackgroundTasks
from starlette.responses import JSONResponse
from database import Products, User, Orders, main
from helps import helper, emails, Middleware
from models import CommentModel, InvoiceModal, PayModel, TransactionModel

router = APIRouter()


def extract_order_data(
        request: Request,
        transact: TransactionModel.Transaction
) -> dict:
    """
    Extract order data.
    :param request:
    :param transact:
    :return:
    """
    transaction_id = transact.transaction
    if transaction_id is None:
        raise ValueError("Transaction cannot be None")

    user_id = request.session.get("user_id")
    if user_id is None:
        raise ValueError("User does not exist")

    cart_raw = request.session.get("cart")
    if not cart_raw:
        raise ValueError("No products")

    delivery = request.session.get("delivery")
    if not delivery:
        raise ValueError("No delivery")

    total_price = transact.cardTotal
    if not total_price or total_price == 0:
        raise ValueError("No total price")

    return {
        "user_id": int(user_id),
        "products": json.loads(cart_raw),
        "delivery": delivery,
        "transaction_id": transaction_id,
        "total": float(total_price),
        "bonus": int(request.session.get("bonus", 0)),
        "discount": int(request.session.get("discount", 0))
    }


@router.post("/create")
async def create_order(
        transact: TransactionModel.Transaction,
        request: Request
):
    """
    Create a new order.
    """
    try:
        data = extract_order_data(request, transact)

        async with main.async_session_maker() as session:
            order_manager = Orders.OrderManager(session)
            await order_manager.create_order(
                products=json.dumps(data["products"]),
                user_id=data["user_id"],
                delivery=json.dumps(data["delivery"]),
                total=data["total"],
                transaction_id=data["transaction_id"],
                bonus=data["bonus"],
                discount=data["discount"]
            )

            user_manager = User.UserManager(session)
            await user_manager.bonus(
                idx=data["user_id"],
                target="add",
                total=int(data["total"] * 2 / 100)
            )

            if data["bonus"]:
                await user_manager.bonus(
                    idx=data["user_id"],
                    target="remove",
                    total=data["bonus"]
                )

            product_manager = Products.ProductManager(session)
            for product_id, amount in data["products"].items():
                await product_manager.set_amount_product(
                    int(product_id),
                    int(amount)
                )

            request.session.pop("cart", None)

        return {"success": True, "data": None, "error": None}

    except ValueError as e:
        logging.warning(e)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"success": False, "data": None, "error": str(e)}
        )


@router.post("/get_orders_user")
async def get_orders_user(request: Request) -> JSONResponse:
    """
    Get orders user
    :param request:
    :return:
    """
    try:
        async with main.async_session_maker() as session:
            user_id = request.session.get("user_id")
            if user_id is None:
                raise HTTPException(status_code=401, detail="Missing user_id")
            order_manager = Orders.OrderManager(session)
            orders = await order_manager.get_orders_user(int(user_id))
            if not orders:
                raise HTTPException(status_code=400, detail="No orders")
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": {"orders": orders},
                    "error": None
                }
            )
    except HTTPException as e:
        logging.exception(e.detail)
        return JSONResponse(
            status_code=e.status_code,
            content={
                "success": False,
                "data": None,
                "error": e.detail
            }
        )


@router.post("/pay")
async def pay(pay_: PayModel.Pay):
    """
    Create a payment.
    :param pay_:
    :return:
    """
    try:
        pay_total = pay_.cardTotal
        if pay_total <= 0:
            raise ValueError("Total is zero")
        clean_number = pay_.cardNumber.replace(" ", "")
        if not re.fullmatch(r"\d{16}", clean_number):
            raise ValueError("Invalid card number")
        month = int(pay_.cardMonth)
        if not 1 <= month <= 12:
            raise ValueError("Invalid expiry month")
        year = int("20" + pay_.cardYear)
        current_year = int(datetime.now().strftime("%Y"))
        if year < current_year:
            raise ValueError("Invalid data year")
        if not re.fullmatch(r"\d{3,4}", pay_.cardKey):
            raise ValueError("Invalid CVV")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "data": {"transaction_id": helper.generate_transaction()},
                "error": None
            }
        )
    except ValueError as e:
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
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Missing user_id")
        admin = await Middleware.is_admin(int(user_id))
        if not admin:
            raise HTTPException(status_code=403, detail="Permission denied")
        async with main.async_session_maker() as session:
            order_manager = Orders.OrderManager(session)
            orders = await order_manager.get_orders()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": {"orders": orders},
                    "error": None
                }
            )
    except HTTPException as e:
        logging.exception(e.detail)
        return JSONResponse(
            status_code=e.status_code,
            content={
                "success": False,
                "data": None,
                "error": e.detail
            }
        )


@router.post("/send_invoice/{idx}/{order_id}")
async def send_invoice(
        idx: int,
        order_id: int,
        invoice: InvoiceModal.Invoice,
        request: Request,
        background_task: BackgroundTasks
) -> JSONResponse:
    """
    Send invoice
    :param background_task:
    :param order_id:
    :param idx:
    :param invoice:
    :param request:
    :return:
    """
    try:
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Missing user_id")
        admin = await Middleware.is_admin(int(user_id))
        if not admin:
            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )
        async with main.async_session_maker() as session:
            order_manager = Orders.OrderManager(session)
            orders = await order_manager.set_invoice_order(
                idx=int(order_id),
                invoice=invoice.body,
            )
            if orders is False:
                raise HTTPException(
                    status_code=400,
                    detail="Invoice order failed"
                )
            user_manager = User.UserManager(session)
            user = await user_manager.get_user(int(idx))
            if user is None:
                raise HTTPException(
                    status_code=400,
                    detail="Fetch user failed"
                )
            background_task.add_task(
                emails.send_emails,
                header="Send invoice",
                title="Invoice",
                body=f"Your invoice: {invoice.body}",
                idx=int(idx),
                email=user['email'],
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
    except HTTPException as e:
        logging.exception(e.detail)
        return JSONResponse(
            status_code=e.status_code,
            content={
                "success": False,
                "data": None,
                "error": e.detail
            }
        )


@router.post("/add_comment/{idx}")
async def add_comment(
        idx: int,
        comment: CommentModel.Comment,
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
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Missing user_id")
        admin = await Middleware.is_admin(int(user_id))
        if not admin:
            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )
        async with main.async_session_maker() as session:
            order_manager = Orders.OrderManager(session)
            orders = await order_manager.add_comment(
                idx=int(idx),
                comment=comment.body,
            )
            if orders is False:
                raise HTTPException(
                    status_code=400,
                    detail="Invoice order failed"
                )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": None,
                    "error": None
                }
            )
    except HTTPException as e:
        logging.exception(e.detail)
        return JSONResponse(
            status_code=e.status_code,
            content={
                "success": False,
                "data": None,
                "error": e.detail
            }
        )


def extract_order_view_data(idx: int, request: Request) -> dict:
    """
    Extract order view data
    :param idx:
    :param request:
    :return:
    """
    user_id = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Missing user_id")
    if not Middleware.is_admin(int(user_id)):
        raise HTTPException(status_code=403, detail="Permission denied")
    return {"user_id": int(user_id), "order_id": idx}


async def prepare_get_order_view_args(idx: int, request: Request) -> dict:
    """
    Prepare get order view args
    :param idx:
    :param request:
    :return:
    """
    user_id = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Missing user_id")
    if not await Middleware.is_admin(int(user_id)):
        raise HTTPException(status_code=403, detail="Admin access required")
    return {
        "user_id": int(user_id),
        "order_id": int(idx)
    }


async def map_order_products(product_manager, products_dict: dict) -> list:
    """
    Map products to orders
    :param product_manager:
    :param products_dict:
    :return:
    """
    products_ = []
    for pid, amount in products_dict.items():
        product = await product_manager.get_product(pid)
        if product:
            pd = product.to_dict() if hasattr(product, "to_dict") else {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "description": product.description,
                "amounts": product.amount
            }
            pd["amount"] = amount
            products_.append(pd)
    return products_


@router.post("/get_view/{idx}")
async def get_order_view(idx: int, request: Request):
    """
    Get order view
    :param idx:
    :param request:
    :return:
    """
    try:
        args = await prepare_get_order_view_args(idx, request)

        async with main.async_session_maker() as session:
            order_manager = Orders.OrderManager(session)
            order = await order_manager.get_order(idx=args["order_id"])
            if not order:
                raise HTTPException(status_code=400, detail="Order not found")

            products_dict = json.loads(order.products)
            product_manager = Products.ProductManager(session)
            products_ = await map_order_products(
                product_manager,
                products_dict
            )
            delivery_data = json.loads(json.loads(order.delivery))
            delivery = await order_manager.get_delivery(**{
                "post_id": int(delivery_data["post_id"]),
                "city_id": int(delivery_data["city_id"]),
                "address_id": int(delivery_data["address"])
            })

            user_ = {
                "first_name": order.user.first_name,
                "last_name": order.user.last_name,
                "phone": order.user.phone,
                "email": order.user.email
            }

            data = {
                "id": order.id,
                "delivery": delivery,
                "user": user_,
                "total": order.total,
                "created": order.created_at.strftime("%d-%m-%Y"),
                "invoice": order.invoice,
                "products": products_,
                "bonus": order.bonus,
                "discount": order.discount
            }

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": data,
                "error": None
            })
    except HTTPException as e:
        logging.exception(e.detail)
        return JSONResponse(
            status_code=e.status_code,
            content={
                "success": False,
                "data": None,
                "error": e.detail
            }
        )


@router.post("/get_predict/{n}")
async def get_predict(n: int, request: Request) -> JSONResponse:
    """
    Get predict
    :param n:
    :param request:
    :return:
    """
    try:
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Missing user_id"
            )
        admin = await Middleware.is_admin(int(user_id))
        if not admin:
            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )
        async with main.async_session_maker() as session:
            order_manager = Orders.OrderManager(session)
            orders = await order_manager.get_predict(term=int(n))
            if not orders:
                raise HTTPException(
                    status_code=400,
                    detail="Get predict failed"
                )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": {"predict": orders},
                    "error": None
                }
            )
    except HTTPException as e:
        logging.exception(e.detail)
        return JSONResponse(
            status_code=e.status_code,
            content={
                "success": False,
                "data": None,
                "error": e.detail
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
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Missing user_id")
        admin = await Middleware.is_admin(int(user_id))
        if not admin:
            raise HTTPException(status_code=403, detail="Permission denied")
        async with main.async_session_maker() as session:
            order_manager = Orders.OrderManager(session)
            orders = await order_manager.delete_order(
                idx=int(idx)
            )
            if orders is False:
                raise HTTPException(
                    status_code=400,
                    detail="Delete order failed"
                )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": None,
                    "error": None
                }
            )
    except HTTPException as e:
        logging.exception(e.detail)
        return JSONResponse(
            status_code=e.status_code,
            content={
                "success": False,
                "data": None,
                "error": e.detail
            }
        )
