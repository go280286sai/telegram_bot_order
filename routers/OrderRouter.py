import logging
import re
from datetime import datetime
from helps.help import generate_transaction
from fastapi import APIRouter, Request, status, Response
from starlette.responses import JSONResponse
from database.Orders import OrderManager
from database.main import async_session_maker
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
        async with async_session_maker() as session:
            transaction = transact.transaction
            if transaction is None:
                raise Exception("Transaction cannot be None")
            user = request.cookies.get('user_id')
            if not user:
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
            order_manager = OrderManager(session)
            await order_manager.create_order(
                products=products,
                user_id=int(user),
                delivery_id=int(delivery),
                total=float(total_price),
                transaction_id=transaction
            )
            response.delete_cookie("cart")
            return {
                "success": True,
                "data": None,
                "error": None
            }

    except Exception as e:
        logging.exception(e)
        JSONResponse(
            status_code=status.HTTP_200_OK,
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
            print(orders)
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
            status_code=400,
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
        current_year = int(datetime.now().strftime("%y"))
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
        print(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": str(e)
            }
        )
