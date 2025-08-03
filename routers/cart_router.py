"""
Router module for managing user cart-related endpoints.
Includes operations for listing, creating, updating,
add discount, delivery and deleting cart.
"""
import json
import logging

from fastapi import APIRouter, Request, status, HTTPException
from starlette.responses import JSONResponse
from database import Orders, User, Products, main
from helps import helper
from models import DeliveryModel, CartModel

router = APIRouter()


@router.post("/delivery/create")
async def set_delivery(
        delivery: DeliveryModel.Delivery,
        request: Request
) -> JSONResponse:
    """
    Create a new delivery.
    :return:
    """
    try:
        if delivery.post_id is None:
            raise HTTPException(
                status_code=422,
                detail="Post ID is required"
            )
        if delivery.city_id is None:
            raise HTTPException(
                status_code=422,
                detail="City ID is required"
            )
        if delivery.address_id is None:
            raise HTTPException(
                status_code=422,
                detail="Address ID is required"
            )
        data = {
            "post_id": delivery.post_id,
            "city_id": delivery.city_id,
            "address": delivery.address_id
        }
        request.session["delivery"] = json.dumps(data)
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


@router.post("/discount/add/{discount}")
async def add_discount(discount: int, request: Request) -> JSONResponse:
    """
    Add discount to cart.
    :return:
    """
    try:
        if discount is None:
            raise HTTPException(status_code=422, detail="Discount is required")
        data = {
            "discount": discount
        }
        request.session["discount"] = json.dumps(data)
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


@router.post("/delivery/get")
async def get_delivery(request: Request) -> JSONResponse:
    """
    Get a delivery.
    :param request:
    :return:
    """
    try:
        async with main.async_session_maker() as session:
            deliveries = request.session.get("delivery")
            if deliveries is None:
                raise HTTPException(
                    status_code=400,
                    detail="Delivery is not selected"
                )
            order_manager = Orders.OrderManager(session)
            data = json.loads(deliveries)
            query = await order_manager.get_delivery(
                post_id=data["post_id"],
                city_id=data["city_id"],
                address_id=data["address"]
            )
            if query is None:
                raise HTTPException(
                    status_code=400,
                    detail="Delivery not found"
                )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": query,
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


@router.post("/delivery/delete")
async def delete_delivery(request: Request) -> JSONResponse:
    """
    Delete delivery cookie from session
    """
    try:
        delivery = request.session.get("delivery")
        if delivery is None:
            raise HTTPException(
                status_code=422,
                detail="Delivery data not found"
            )
        request.session.pop("delivery")
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


@router.post("/increase/{product_id}")
async def increase_amount(
        product_id: int,
        request: Request) -> JSONResponse:
    """
    Increase the amount of the cart
    :param request:
    :param product_id:
    :return:
    """
    try:
        async with main.async_session_maker() as session:
            cart = request.session.get("cart")
            if cart:
                cart_items = helper.parse_cart(cart)
            else:
                cart_items = {}
            product_manager = Products.ProductManager(session)
            query = await product_manager.get_product(int(product_id))
            if not query:
                raise HTTPException(status_code=400, detail="No data found")
            if product_id not in cart_items:
                cart_items[product_id] = 1
            elif query.amount > cart_items[product_id]:
                cart_items[product_id] += 1
            request.session["cart"] = json.dumps(cart_items)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": {"cart": cart_items},
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


@router.post("/decrease/{product_id}")
async def decrease_amount(
        product_id: int,
        request: Request) -> JSONResponse:
    """
    Decrease the amount of the cart
    :param product_id:
    :param request:
    :return:
    """
    try:
        cart = request.session.get("cart")
        if cart:
            cart_items = helper.parse_cart(cart)
        else:
            cart_items = {}
        if product_id in cart_items:
            if cart_items[product_id] > 1:
                cart_items[product_id] -= 1
            else:
                del cart_items[product_id]
        request.session["cart"] = json.dumps(
            {str(k): v for k, v in cart_items.items()}
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "data": {"cart": cart_items},
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


@router.post("/remove/{product_id}")
async def remove_from_cart(
        product_id: int,
        request: Request) -> JSONResponse:
    """
    Remove product from cart
    :param product_id:
    :param request:
    :return:
    """
    try:
        cart = request.session.get("cart")
        if not cart:
            raise HTTPException(status_code=400, detail="No cart")
        cart_items = helper.parse_cart(cart)
        cart_items.pop(product_id, None)
        request.session["cart"] = json.dumps(
            {str(k): v for k, v in cart_items.items()}
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "data": {"cart": cart_items},
                "error": None
            }
        )
    except HTTPException as e:
        logging.exception(e)
        return JSONResponse(
            status_code=e.status_code,
            content={
                "success": False,
                "data": None,
                "error": e.detail
            }
        )


@router.post("/total_bonus")
async def set_total_bonus(
        cart: CartModel.Cart,
        request: Request
) -> JSONResponse:
    """
    Set total bonus
    :param cart:
    :param request:
    :return:
    """
    try:
        if cart.bonus is None:
            raise HTTPException(status_code=422, detail="Bonus is required")
        if cart.total is None:
            raise HTTPException(status_code=422, detail="Total is required")
        request.session["bonus"] = str(cart.bonus)
        request.session["total"] = str(cart.total)
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


def extract_session_data(request: Request) -> dict:
    """
    Extract session data
    :param request:
    :return:
    """
    session = request.session
    return {
        "user_id": session.get("user_id"),
        "bonus": session.get("bonus", 0),
        "pay_bonus": session.get("bonus", 0),
        "total": session.get("total", 0),
        "cart": session.get("cart", "{}"),
        "discount_raw": session.get("discount")
    }


def get_discount(discount_raw) -> int:
    """
    Extract discount
    :param discount_raw:
    :return:
    """
    if isinstance(discount_raw, str):
        try:
            return json.loads(discount_raw).get("discount", 0)
        except json.JSONDecodeError:
            return 0
    return 0


def serialize_product(product, amount: int, discount: int) -> dict:
    """
    Serialize a product
    :param product:
    :param amount:
    :param discount:
    :return:
    """
    if hasattr(product, "to_dict"):
        data = product.to_dict()
    else:
        data = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description,
            "amounts": product.amount
        }
    data.update({
        "amount": amount,
        "discount": discount
    })
    return data


@router.post("/")
async def get_cart(request: Request) -> JSONResponse:
    """
    Get cart
    :param request:
    :return:
    """
    try:
        data = extract_session_data(request)
        cart_items = helper.parse_cart(data["cart"])
        discount = get_discount(data["discount_raw"])
        async with main.async_session_maker() as session:
            user_manager = User.UserManager(session)
            user = await user_manager.get_user(int(data["user_id"]))
            if user is None:
                raise HTTPException(status_code=400, detail="No user found")
            product_manager = Products.ProductManager(session)
            products_ = []
            for product_id, amount in cart_items.items():
                product = await product_manager.get_product(product_id)
                if product is None:
                    raise HTTPException(
                        status_code=400,
                        detail="No product found"
                    )
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
                "data": {
                    "cart": products_,
                    "bonus": user['bonus'] if user else None,
                    "pay_bonus": data['pay_bonus'],
                    "total": data['total']
                },
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
