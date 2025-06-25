import json
import logging
from typing import Dict, Any

from fastapi import APIRouter, Response, Request, Cookie, status
from helps.help import parse_cart
from database.Products import ProductManager
from database.main import async_session_maker
from starlette.responses import JSONResponse

router = APIRouter()


@router.get("/products")
async def products() -> JSONResponse:
    """
    Get all products
    """
    try:
        async with async_session_maker() as session:
            product_manager = ProductManager(session)
            query = await product_manager.get_products()
            if not query:
                raise Exception("No products")
            products_ = [
                {
                    "id": p.id,
                    "name": p.name,
                    "price": p.price,
                    "description": p.description,
                    "amount": p.amount,
                } for p in query
            ]

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": {"products": products_},
                    "error": None
                }
            )
    except Exception as e:
        logging.exception(f"Failed to fetch products: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed to fetch products"
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
                    product_data["amount"] = min(int(amount or 1),
                                                 int(product.amount or 1))
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
