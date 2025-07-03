import json
import logging

from fastapi import APIRouter, Response, Request, Cookie, status

from database.Deliveries import DeliveryManager
from helps.help import parse_cart
from database.Products import ProductManager
from database.main import async_session_maker
from starlette.responses import JSONResponse

router = APIRouter()


@router.post("/delivery/create/{idx}")
async def set_delivery(idx: int) -> JSONResponse:
    """
    Create a new delivery.
    :return:
    """
    try:
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
            value=str(idx),
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


@router.post("/delivery/get")
async def get_delivery(request: Request) -> JSONResponse:
    """
    Get a delivery.
    :param request:
    :return:
    """
    try:
        async with async_session_maker() as session:
            delivery_id = request.cookies.get("delivery")
            if delivery_id is None:
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        "success": False,
                        "data": None,
                        "error": "Delivery is not selected"
                    }
                )

            delivery_manager = DeliveryManager(session)

            query = await delivery_manager.get_delivery(idx=int(delivery_id))

            if query is None:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
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
async def delete_delivery(request: Request, response: Response) -> JSONResponse:
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
