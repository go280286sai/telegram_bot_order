"""
Router module for managing user address-related endpoints.
Includes operations for listing, creating, updating, and deleting addresses.
"""

import logging

from fastapi import APIRouter, status, Request, HTTPException
from starlette.responses import JSONResponse
from database.main import async_session_maker
from database.Address import AddressManager
from helps.Middleware import is_admin
from models.AddressModel import Address

router = APIRouter()


@router.post("/create")
async def create_address(address: Address, request: Request) -> JSONResponse:
    """
    Create address
    :param request:
    :param address:
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
            address_manager = AddressManager(session)
            query = await address_manager.create_address(
                name=address.name,
                city_id=address.city_id
            )
            if query is None:
                raise HTTPException(
                    status_code=400,
                    detail="Create address failed"
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
async def update_address(
        idx: int,
        address: Address,
        request: Request
) -> JSONResponse:
    """
    Update address
    :param request:
    :param idx:
    :param address:
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
            address_manager = AddressManager(session)
            query = await address_manager.update_address(
                idx=idx,
                name=address.name,
                city_id=address.city_id
            )
            if query is False:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to update address"
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
                raise HTTPException(
                    status_code=400,
                    detail="Failed to get addresses"
                )
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
                raise HTTPException(
                    status_code=400,
                    detail="Failed to fetch address"
                )
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
    Delete address
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
            raise HTTPException(status_code=403, detail="Permission denied")
        async with async_session_maker() as session:
            address_manager = AddressManager(session)
            query = await address_manager.delete_address(idx=idx)
            if query is False:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to delete address"
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
