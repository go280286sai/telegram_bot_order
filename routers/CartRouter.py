import json
import logging

from fastapi import APIRouter, Response, Request, Cookie, status

from database.Orders import OrderManager
from helps.help import parse_cart
from database.Products import ProductManager
from database.main import async_session_maker
from models.DeliveryModel import Delivery
from starlette.responses import JSONResponse

router = APIRouter()


@router.post("/delivery/create")
async def set_delivery(delivery: Delivery) -> JSONResponse:
    """
    Create a new delivery.
    :return:
    """
    try:
        data = {
            "post_id": delivery.post_id,
            "city_id": delivery.city_id,
            "address": delivery.address_id
        }
        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "data": None,
                "error": None
            }
        )
        response.set_cookie(
            key="delivery",
            value=json.dumps(data),
            httponly=True)
        return response
    except Exception as e:
        logging.exception(f"Delivery registration failed {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Delivery registration failed"
            }
        )


@router.post("/discount/add/{discount}")
async def add_discount(discount: int) -> JSONResponse:
    """
    Add discount to cart.
    :return:
    """
    try:
        data = {
            "discount": discount
        }
        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "data": None,
                "error": None
            }
        )
        response.set_cookie(
            key="discount",
            value=json.dumps(data),
            httponly=True)
        return response
    except Exception as e:
        logging.exception(f"Discount add error {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Discount add error "
            }
        )


@router.post("/delivery/get")
async def get_delivery(request: Request) -> JSONResponse:
    """
    Get a delivery.
    :param request:
    :return:
    """
    try:
        async with async_session_maker() as session:
            deliveries = request.cookies.get("delivery")
            if deliveries is None:
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        "success": False,
                        "data": None,
                        "error": "Delivery is not selected"
                    }
                )

            order_manager = OrderManager(session)
            data = json.loads(deliveries)
            query = await order_manager.get_delivery(
                post_id=data["post_id"],
                city_id=data["city_id"],
                address_id=data["address"]
            )
            if query is None:
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        "success": False,
                        "data": None,
                        "error": "Delivery not found"
                    }
                )

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": query,
                    "error": None
                }
            )

    except Exception as e:
        logging.exception("Failed to get delivery")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "data": None,
                "error": str(e)
            }
        )


@router.post("/delivery/delete")
async def delete_delivery(request: Request) -> JSONResponse:
    """
    Delete delivery cookie from session
    """
    try:
        delivery = request.cookies.get("delivery")

        if delivery is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "data": None,
                    "error": "Delivery cookie not found"
                }
            )

        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "data": None,
                "error": None
            }
        )
        response.delete_cookie("delivery")
        return response
    except Exception as e:
        logging.exception(f"Delivery is failed {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Delivery is failed"
            }
        )


@router.post("/increase/{product_id}")
async def increase_amount(
        product_id: int,
        response: Response,
        cart: str = Cookie(default="{}")) -> dict:
    """
    Increase the amount of the cart
    :param product_id:
    :param response:
    :param cart:
    :return:
    """
    try:
        async with async_session_maker() as session:
            cart_items = parse_cart(cart)
            product_manager = ProductManager(session)
            query = await product_manager.get_product(int(product_id))
            if not query:
                raise Exception("No product")
            if product_id not in cart_items:
                cart_items[product_id] = 1
            elif query.amount > cart_items[product_id]:
                cart_items[product_id] += 1
            response.set_cookie(
                key="cart",
                value=json.dumps(cart_items),
                httponly=True
            )
    except Exception as e:
        logging.exception(f"Failed to increase item in cart: {e}")
    finally:
        return {"success": True, "data": {"cart": cart_items}, "error": None}


@router.post("/decrease/{product_id}")
async def decrease_amount(
        product_id: int,
        response: Response,
        cart: str = Cookie(default="{}")) -> dict:
    cart_items = parse_cart(cart)
    try:
        if product_id in cart_items:
            if cart_items[product_id] > 1:
                cart_items[product_id] -= 1
            else:
                del cart_items[product_id]
        response.set_cookie(
            key="cart",
            value=json.dumps({str(k): v for k, v in cart_items.items()}),
            httponly=True
        )
    except Exception as e:
        logging.exception(f"Failed to decrease item in cart: {e}")
    finally:
        return {"success": True, "data": {"cart": cart_items}, "error": None}


@router.post("/remove/{product_id}")
async def remove_from_cart(
        product_id: int,
        response: Response,
        cart: str = Cookie(default="{}")) -> dict:
    try:
        cart_items = parse_cart(cart)
        cart_items.pop(product_id, None)
        response.set_cookie(
            key="cart",
            value=json.dumps({str(k): v for k, v in cart_items.items()}),
            httponly=True
        )
    except Exception as e:
        logging.exception(f"Failed to remove item from cart: {e}")
    finally:
        return {"success": True, "data": {"cart": cart_items}, "error": None}


@router.post("/")
async def get_cart(request: Request) -> JSONResponse:
    try:
        raw_cart_cookie = request.cookies.get("cart", "{}")
        cart_items = parse_cart(raw_cart_cookie)
        discount_raw = request.cookies.get('discount')
        if discount_raw:
            if isinstance(discount_raw, str):
                discount = json.loads(discount_raw).get("discount", 0)
            else:
                discount = 0
        else:
            discount = 0
        async with async_session_maker() as session:
            product_manager = ProductManager(session)
            products_ = []

            for product_id, amount in cart_items.items():
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
                    product_data["discount"] = discount
                    products_.append(product_data)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "data": {"cart": products_},
                "error": None
            }
        )
    except Exception as e:
        logging.exception(f"Failed to fetch cart: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed to retrieve cart"
            }
        )
