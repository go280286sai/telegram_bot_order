"""
Router module for managing user city-related endpoints.
Includes operations for listing, creating, updating, and deleting cities.
"""
import logging

from fastapi import APIRouter, status, Request, HTTPException
from starlette.responses import JSONResponse
from database.main import async_session_maker
from database.City import CityManager
from helps.Middleware import is_admin
from models.CityModel import City

router = APIRouter()


@router.post("/create")
async def create_city(city: City, request: Request) -> JSONResponse:
    """
    Create city
    :param request:
    :param city:
    :return:
    """
    try:
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="User not authenticated"
            )
        admin = await is_admin(int(user_id))
        if admin is None or admin is False:
            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )
        async with async_session_maker() as session:
            city_manager = CityManager(session)
            query = await city_manager.create_city(
                name=city.name,
                post_id=city.post_id
            )
            if query is None:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to create city"
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
async def update_city(idx: int, city: City, request: Request) -> JSONResponse:
    """
    Update city
    :param request:
    :param idx:
    :param city:
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
            city_manager = CityManager(session)
            query = await city_manager.update_city(
                idx=idx,
                name=city.name,
                post_id=city.post_id
            )
            if query is False:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to update city"
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


@router.get("/get/{post_id}")
async def get_address(post_id: int) -> JSONResponse:
    """
    Get cities
    :return:
    """
    try:
        async with async_session_maker() as session:
            address_manager = CityManager(session)
            query = await address_manager.get_city(int(post_id))
            if query is None:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to fetch cities"
                )
            cities_ = [
                {
                    "id": p.id,
                    "name": p.name,
                } for p in query
            ]

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": {"cities": cities_},
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


@router.get("/gets")
async def get_city() -> JSONResponse:
    """
    Get city
    :return:
    """
    try:
        async with async_session_maker() as session:
            city_manager = CityManager(session)
            query = await city_manager.get_cities()
            if query is None:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to get city"
                )
            city_ = [
                {
                    "id": p.id,
                    "name": p.name,
                    "post_id": p.post_id
                } for p in query
            ]
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": {"cities": city_},
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
async def delete_city(idx: int, request: Request) -> JSONResponse:
    """
    Delete city
    :param request:
    :param idx:
    :return:
    """
    try:
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=422, detail="Missing user_id")
        admin = await is_admin(int(user_id))
        if not admin:
            raise HTTPException(status_code=403, detail="Permission denied")
        async with async_session_maker() as session:
            city_manager = CityManager(session)
            query = await city_manager.delete_city(idx=idx)
            if query is False:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to delete city"
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
