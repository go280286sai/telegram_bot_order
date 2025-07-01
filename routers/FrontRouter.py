import logging

from fastapi import APIRouter, status
from starlette.responses import JSONResponse
from database.main import async_session_maker
from database.Carousel import CarouselManager
from models.CarouselModel import Carousel

router = APIRouter()


@router.post("/carousel/create")
async def create_item(carousel: Carousel) -> JSONResponse:
    """
    Create a carousel item
    :param carousel:
    :return:
    """
    try:
        async with async_session_maker() as session:
            carousel_manager = CarouselManager(session)
            query = await carousel_manager.create_item(
                title=carousel.title,
                description=carousel.description,
                image=carousel.image
            )
            if query is False:
                raise Exception("Failed to create carousel")
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
                "error": "Failed to create carousel"
            }
        )


@router.post("/carousel/update/{idx}")
async def update_item(idx: int, carousel: Carousel) -> JSONResponse:
    """
    Update a carousel item
    :param idx:
    :param carousel:
    :return:
    """
    try:
        async with async_session_maker() as session:
            carousel_manager = CarouselManager(session)
            query = await carousel_manager.update_item(
                idx=idx,
                title=carousel.title,
                description=carousel.description,
                image=carousel.image
            )
            if query is False:
                raise Exception("Failed to update carousel")
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
                "error": "Failed to update carousel"
            }
        )


@router.get("/carousel/gets")
async def get_item() -> JSONResponse:
    """
    Get all carousel items
    :return:
    """
    try:
        async with async_session_maker() as session:
            carousel_manager = CarouselManager(session)
            query = await carousel_manager.get_items()
            if query is None:
                raise Exception("Failed to get carousels")
            carousels_ = [
                {
                    "id": p.id,
                    "title": p.title,
                    "description": p.description,
                    "image": p.image,
                } for p in query
            ]

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": {"carousels": carousels_},
                    "error": None
                }
            )
    except Exception as e:
        logging.exception(f"Failed to fetch carousels: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed to fetch carousels"
            }
        )


@router.post("/carousel/delete/{idx}")
async def delete_item(idx: int) -> JSONResponse:
    """
    Delete item
    """
    try:
        async with async_session_maker() as session:
            carousel_manager = CarouselManager(session)
            query = await carousel_manager.delete_items(idx=idx)
            if query is False:
                raise Exception("Failed to delete carousel")
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": None,
                    "error": None
                }
            )
    except Exception as e:
        logging.exception(f"Failed to fetch carousels: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed to delete carousel"
            }
        )
