import logging

from fastapi import APIRouter, status
from starlette.responses import JSONResponse
from database.main import async_session_maker
from database.Address import AddressManager
from models.AddressModel import Address

router = APIRouter()


@router.post("/create")
async def create_address(address: Address) -> JSONResponse:
    """
    Create address
    :param address:
    :return:
    """
    try:
        async with async_session_maker() as session:
            address_manager = AddressManager(session)
            query = await address_manager.create_address(
                name=address.name,
                city_id=address.city_id
            )
            if query is False:
                raise Exception("Failed to create address")
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
                "error": "Failed to create address"
            }
        )


@router.post("/update/{idx}")
async def update_address(idx: int, address: Address) -> JSONResponse:
    """
    Update address
    :param idx:
    :param address:
    :return:
    """
    try:
        async with async_session_maker() as session:
            address_manager = AddressManager(session)
            query = await address_manager.update_address(
                idx=idx,
                name=address.name,
                city_id=address.city_id
            )
            if query is False:
                raise Exception("Failed to update address")
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
                "error": "Failed to update address"
            }
        )


@router.get("/gets")
async def get_addresses() -> JSONResponse:
    """
    Get addresses
    :return:
    """
    try:
        async with async_session_maker() as session:
            address_manager = AddressManager(session)
            query = await address_manager.get_addresses()
            if query is None:
                raise Exception("Failed to get address")
            address_ = [
                {
                    "id": p.id,
                    "name": p.name,
                    "city_id": p.city_id
                } for p in query
            ]

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": {"addresses": address_},
                    "error": None
                }
            )
    except Exception as e:
        logging.exception(f"Failed to fetch address: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed to fetch address"
            }
        )


@router.get("/get/{city_id}")
async def get_address(city_id: int) -> JSONResponse:
    """
    Get address
    :return:
    """
    try:
        async with async_session_maker() as session:
            address_manager = AddressManager(session)
            query = await address_manager.get_address(int(city_id))
            if query is None:
                raise Exception("Failed to get address")
            address_ = [
                {
                    "id": p.id,
                    "name": p.name,
                } for p in query
            ]

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": {"addresses": address_},
                    "error": None
                }
            )
    except Exception as e:
        logging.exception(f"Failed to fetch address: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed to fetch address"
            }
        )


@router.post("/delete/{idx}")
async def delete_city(idx: int) -> JSONResponse:
    """
    Delete address
    :param idx:
    :return:
    """
    try:
        async with async_session_maker() as session:
            address_manager = AddressManager(session)
            query = await address_manager.delete_address(idx=idx)
            if query is False:
                raise Exception("Failed to delete address")
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": None,
                    "error": None
                }
            )
    except Exception as e:
        logging.exception(f"Failed to fetch address: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed to delete address"
            }
        )
