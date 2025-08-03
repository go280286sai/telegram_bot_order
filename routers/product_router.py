"""
Router module for managing user product-related endpoints.
Includes operations for listing, creating, updating, and deleting product.
"""
import logging

from fastapi import APIRouter, status, Request, HTTPException
from starlette.responses import JSONResponse
from database import Products, main
from helps.Middleware import is_admin
from models.ProductModel import Product

router = APIRouter()


@router.post("/create")
async def product_create(item: Product, request: Request) -> JSONResponse:
    """
    Create a new product.
    :param request:
    :param item:
    :return:
    """
    try:
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Missing user_id")
        admin = await is_admin(int(user_id))
        if not admin:
            raise HTTPException(status_code=403, detail="Permission denied")
        async with main.async_session_maker() as session:
            product_manager = Products.ProductManager(session)
            query = await product_manager.create_product(
                name=item.name,
                description=item.description,
                price=item.price,
                amount=item.amount
            )
            if query is None:
                raise HTTPException(
                    status_code=400,
                    detail="Error creating product"
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


@router.post("/update/{idx}")
async def product_update(
        idx: int,
        item: Product,
        request: Request
) -> JSONResponse:
    """
    Update an existing product.
    :param request:
    :param idx:
    :param item:
    :return:
    """
    try:
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Missing user_id")
        admin = await is_admin(int(user_id))
        if not admin:
            raise HTTPException(status_code=403, detail="Permission denied")
        async with main.async_session_maker() as session:
            product_manager = Products.ProductManager(session)
            query = await product_manager.update_product(
                idx=idx,
                name=item.name,
                description=item.description,
                price=item.price,
                amount=item.amount,
                service=item.service
            )
            if query is False:
                raise HTTPException(
                    status_code=400,
                    detail="Error updating product"
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


@router.get("/products")
async def products() -> JSONResponse:
    """
    Get all products.
    :return:
    """
    try:
        async with main.async_session_maker() as session:
            product_manager = Products.ProductManager(session)
            query = await product_manager.get_products()
            if query is None:
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        "success": True,
                        "data": None,
                        "error": None
                    }
                )
            products_ = [
                {
                    "id": p.id,
                    "name": p.name,
                    "price": p.price,
                    "description": p.description,
                    "amount": p.amount,
                    "service": p.service
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


@router.post("/product/{idx}")
async def product(idx: int) -> JSONResponse:
    """
    Create a new product.
    :param idx:
    :return:
    """
    try:
        async with main.async_session_maker() as session:
            product_manager = Products.ProductManager(session)
            query = await product_manager.get_product(idx=idx)
            if query is None:
                raise HTTPException(status_code=400, detail="No products")
            product_ = [
                {
                    "id": query.id,
                    "name": query.name,
                    "price": query.price,
                    "description": query.description,
                    "amount": query.amount,
                }
            ]

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": {"products": product_},
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
async def product_delete(idx: int, request: Request) -> JSONResponse:
    """
    Delete an existing product.
    :param request:
    :param idx:
    :return:
    """
    try:
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Missing user_id")
        admin = await is_admin(int(user_id))
        if not admin:
            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )
        async with main.async_session_maker() as session:
            product_manager = Products.ProductManager(session)
            query = await product_manager.delete_product(idx=idx)
            if query is False:
                raise HTTPException(
                    status_code=400,
                    detail="Error deleting product"
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
