import logging

from fastapi import APIRouter, status
from starlette.responses import JSONResponse
from database.main import async_session_maker
from database.Setting import SettingManager
from models.SettingModel import Setting

router = APIRouter()


@router.post("/create")
async def create_setting(setting_: Setting) -> JSONResponse:
    """
    Create setting
    :param setting_:
    :return:
    """
    try:
        async with async_session_maker() as session:
            setting_manager = SettingManager(session)
            query = await setting_manager.create_setting(
                name=setting_.name,
                value=setting_.value,
            )
            if query is None:
                raise Exception("Failed to create setting")
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
                "error": "Failed to create setting"
            }
        )


@router.post("/auto_create")
async def auto_create_setting() -> JSONResponse:
    """
    Create auto settings
    :return:
    """
    auto_fill = {
        "title": "",
        "description": "",
        "telegram": "",
        "viber": "",
        "whatsapp": "",
        "phone": "",
        "email": "",
        "address": "",
        "map": "",
        "promotional": "",
        "discount": ""
    }
    try:
        async with async_session_maker() as session:
            setting_manager = SettingManager(session)
            for key, value in auto_fill.items():
                query = await setting_manager.create_setting(
                    name=key,
                    value=value,
                )
            if query is None:
                raise Exception("Failed to create setting")
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
                "error": "Failed to create setting"
            }
        )


@router.post("/update/{idx}")
async def update_setting(idx: int, setting_: Setting) -> JSONResponse:
    """
    Update setting
    :param idx:
    :param setting_:
    :return:
    """
    try:
        async with async_session_maker() as session:
            setting_manager = SettingManager(session)
            query = await setting_manager.update_setting(
                idx=idx,
                name=setting_.name,
                value=setting_.value,
            )
            if query is False:
                raise Exception("Failed to update setting")
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
                "error": "Failed to update setting"
            }
        )


@router.get("/gets")
async def get_setting() -> JSONResponse:
    """
    Get settings
    :return:
    """
    try:
        async with async_session_maker() as session:
            setting_manager = SettingManager(session)
            query = await setting_manager.get_settings()
            if query is None:
                raise Exception("Failed to get setting")
            settings_ = [
                {
                    "id": p.id,
                    "name": p.name,
                    "value": p.value
                } for p in query
            ]

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": {"settings": settings_},
                    "error": None
                }
            )
    except Exception as e:
        logging.exception(f"Failed to fetch settings: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed to fetch settings"
            }
        )


@router.get("/get/discount")
async def get_discount() -> JSONResponse:
    """
    Get discount
    :return:
    """
    try:
        async with async_session_maker() as session:
            setting_manager = SettingManager(session)
            query = await setting_manager.get_settings()
            if query is None:
                raise Exception("Failed to get setting")
            dic = {}
            settings_ = [
                dic.update({setting.name: setting.value})
                for setting in query
                if setting.name in {"discount", "promotional"}
            ]
            if not settings_:
                raise Exception("No matching settings found")
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": {"settings": dic},
                    "error": None
                }
            )
    except Exception as e:
        logging.exception(f"Failed to fetch settings: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed to fetch settings"
            }
        )


@router.post("/delete/{idx}")
async def delete_setting(idx: int) -> JSONResponse:
    """
    Delete setting
    :param idx:
    :return:
    """
    try:
        async with async_session_maker() as session:
            setting_manager = SettingManager(session)
            query = await setting_manager.delete_setting(idx=idx)
            if query is False:
                raise Exception("Failed to delete setting")
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": None,
                    "error": None
                }
            )
    except Exception as e:
        logging.exception(f"Failed to fetch setting: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed to delete setting"
            }
        )
