import logging

from fastapi import APIRouter, status
from database.Products import ProductManager
from database.main import async_session_maker
from starlette.responses import JSONResponse
from models.ProductModel import Product

router = APIRouter()


@router.post("/create")
async def product_create(item: Product) -> JSONResponse:
    """
    Create a new product.
    :param item:
    :return:
    """
    try:
        async with async_session_maker() as session:
            product_manager = ProductManager(session)
            query = await product_manager.create_product(
                name=item.name,
                description=item.description,
                price=item.price,
                amount=item.amount
            )
            if query is False:
                raise Exception("Error creating product")

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": None,
                    "error": None
                }
            )
    except Exception as e:
        logging.exception(f"Error creating product: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Error creating product"
            }
        )


@router.post("/update/{idx}")
async def product_update(idx: int, item: Product) -> JSONResponse:
    """
    Update an existing product.
    :param idx:
    :param item:
    :return:
    """
    try:
        async with async_session_maker() as session:
            product_manager = ProductManager(session)
            query = await product_manager.update_product(
                idx=idx,
                name=item.name,
                description=item.description,
                price=item.price,
                amount=item.amount
            )
            if query is False:
                raise Exception("Error updating product")

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": None,
                    "error": None
                }
            )
    except Exception as e:
        logging.exception(f"Error updating product: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Error updating product"
            }
        )


@router.get("/products")
async def products() -> JSONResponse:
    """
    Get all products.
    :return:
    """
    try:
        async with async_session_maker() as session:
            product_manager = ProductManager(session)
            query = await product_manager.get_products()
            # if query is None:
            #     return JSONResponse(
            #         status_code=status.HTTP_200_OK,
            #         content={
            #             "success": True,
            #             "data": None,
            #             "error": None
            #         }
            #     )
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


@router.post("/product/{idx}")
async def product(idx: int) -> JSONResponse:
    """
    Create a new product.
    :param idx:
    :return:
    """
    try:
        async with async_session_maker() as session:
            product_manager = ProductManager(session)
            query = await product_manager.get_product(idx=idx)
            if not query:
                raise Exception("No products")
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


@router.post("/delete/{idx}")
async def product_delete(idx: int) -> JSONResponse:
    """
    Delete an existing product.
    :param idx:
    :return:
    """
    try:
        async with async_session_maker() as session:
            product_manager = ProductManager(session)
            query = await product_manager.delete_product(idx=idx)
            if query is False:
                raise Exception("Error deleting product")

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": None,
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
