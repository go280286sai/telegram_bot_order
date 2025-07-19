import logging

from fastapi import APIRouter, status
from starlette.responses import JSONResponse
from database.main import async_session_maker
from database.City import CityManager
from models.CityModel import City

router = APIRouter()


@router.post("/create")
async def create_city(city: City) -> JSONResponse:
    """
    Create city
    :param city:
    :return:
    """
    try:
        async with async_session_maker() as session:
            city_manager = CityManager(session)
            query = await city_manager.create_city(
                name=city.name,
                post_id=city.post_id
            )
            if query is None:
                raise Exception()
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
                "error": "Failed to create city"
            }
        )


@router.post("/update/{idx}")
async def update_city(idx: int, city: City) -> JSONResponse:
    """
    Update city
    :param idx:
    :param city:
    :return:
    """
    try:
        async with async_session_maker() as session:
            city_manager = CityManager(session)
            query = await city_manager.update_city(
                idx=idx,
                name=city.name,
                post_id=city.post_id
            )
            if query is False:
                raise Exception("Failed to update city")
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
                "error": "Failed to update city"
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
                raise Exception()
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
    except Exception as e:
        logging.exception(f"Failed to fetch cities: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed to fetch cities"
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
                raise Exception("Failed to get city")
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
    except Exception as e:
        logging.exception(f"Failed to fetch city: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed to fetch city"
            }
        )


@router.post("/delete/{idx}")
async def delete_city(idx: int) -> JSONResponse:
    """
    Delete city
    :param idx:
    :return:
    """
    try:
        async with async_session_maker() as session:
            city_manager = CityManager(session)
            query = await city_manager.delete_city(idx=idx)
            if query is False:
                raise Exception("Failed to delete city")
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": None,
                    "error": None
                }
            )
    except Exception as e:
        logging.exception(f"Failed to fetch city: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed to delete city"
            }
        )
