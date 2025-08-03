"""
Router module for managing user frontend-related endpoints.
Includes operations for listing, creating, updating, and deleting carousel.
"""
import logging

from fastapi import APIRouter, status, Request, HTTPException
from starlette.responses import JSONResponse
from database.main import async_session_maker
from database.Carousel import CarouselManager
from helps.Middleware import is_admin
from models.CarouselModel import Carousel

router = APIRouter()


@router.post("/carousel/create")
async def create_item(carousel: Carousel, request: Request) -> JSONResponse:
    """
    Create a carousel item
    :param request:
    :param carousel:
    :return:
    """
    try:
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Missing user_id")
        admin = await is_admin(int(user_id))
        if not admin:
            raise HTTPException(status_code=403, detail="Permission denied")
        async with async_session_maker() as session:
            carousel_manager = CarouselManager(session)
            query = await carousel_manager.create_item(
                title=carousel.title,
                description=carousel.description,
                image=carousel.image
            )
            if query is False:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to create carousel"
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


@router.post("/carousel/update/{idx}")
async def update_item(
        idx: int,
        carousel: Carousel,
        request: Request
) -> JSONResponse:
    """
    Update a carousel item
    :param request:
    :param idx:
    :param carousel:
    :return:
    """
    try:
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Missing user_id")
        admin = await is_admin(int(user_id))
        if not admin:
            raise HTTPException(status_code=403, detail="Permission denied")
        async with async_session_maker() as session:
            carousel_manager = CarouselManager(session)
            query = await carousel_manager.update_item(
                idx=idx,
                title=carousel.title,
                description=carousel.description,
                image=carousel.image
            )
            if query is False:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to update carousel"
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
                raise HTTPException(
                    status_code=400,
                    detail="Failed to get carousels"
                )
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


@router.post("/carousel/delete/{idx}")
async def delete_item(idx: int, request: Request) -> JSONResponse:
    """
    Delete item
    """
    try:
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Missing user_id")
        admin = await is_admin(int(user_id))
        if not admin:
            raise HTTPException(status_code=403, detail="Permission denied")
        async with async_session_maker() as session:
            carousel_manager = CarouselManager(session)
            query = await carousel_manager.delete_items(idx=idx)
            if query is False:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to delete carousel"
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
