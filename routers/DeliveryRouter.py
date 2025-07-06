import logging

from fastapi import APIRouter, status
from starlette.responses import JSONResponse
from database.main import async_session_maker
from database.Deliveries import DeliveryManager
from models.DeliveryModel import Delivery

router = APIRouter()


@router.post("/create")
async def create_delivery(delivery: Delivery) -> JSONResponse:
    """
    Create delivery
    :param delivery:
    :return:
    """
    try:
        async with async_session_maker() as session:
            delivery_manager = DeliveryManager(session)
            query = await delivery_manager.create_delivery(
                post_id=delivery.post_id,
                city_id=delivery.city_id,
                address_id=delivery.address_id
            )
            if query is False:
                raise Exception("Failed to create delivery")
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": None,
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
                "error": "Failed to create delivery"
            }
        )


@router.post("/update/{idx}")
async def update_delivery(idx: int, delivery: Delivery) -> JSONResponse:
    """
    Update delivery
    :param idx:
    :param delivery:
    :return:
    """
    try:
        async with async_session_maker() as session:
            delivery_manager = DeliveryManager(session)
            query = await delivery_manager.update_delivery(
                idx=idx,
                post_id=delivery.post_id,
                city_id=delivery.city_id,
                address_id=delivery.address_id
            )
            if query is False:
                raise Exception("Failed to update delivery")
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": None,
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
                "error": "Failed to update delivery"
            }
        )


@router.post("/get/{idx}")
async def get_delivery(idx: int) -> JSONResponse:
    """
    Get delivery
    :return:
    """
    try:
        async with async_session_maker() as session:
            delivery_manager = DeliveryManager(session)
            query = await delivery_manager.get_delivery(idx=idx)
            if query is None:
                raise Exception("Failed to get delivery")

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": query,
                    "error": None
                }
            )
    except Exception as e:
        logging.exception(f"Failed to fetch delivery: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed to fetch deliveries"
            }
        )


@router.get("/gets")
async def get_deliveries() -> JSONResponse:
    """
    Get deliveries
    :return:
    """
    try:
        async with async_session_maker() as session:
            delivery_manager = DeliveryManager(session)
            query = await delivery_manager.get_deliveries()
            if query is None:
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        "success": True,
                        "data": None,
                        "error": None
                    }
                )

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": {"deliveries": query},
                    "error": None
                }
            )
    except Exception as e:
        logging.exception(f"Failed to fetch deliveries: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed to fetch deliveries"
            }
        )


@router.post("/delete/{idx}")
async def delete_item(idx: int) -> JSONResponse:
    """
    Delete delivery
    :param idx:
    :return:
    """
    try:
        async with async_session_maker() as session:
            delivery_manager = DeliveryManager(session)
            query = await delivery_manager.delete_delivery(idx=idx)
            if query is False:
                raise Exception("Failed to delete delivery")
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": None,
                    "error": None
                }
            )
    except Exception as e:
        logging.exception(f"Failed to fetch delivery: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed to delete delivery"
            }
        )
