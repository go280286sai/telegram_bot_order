import logging

from fastapi import APIRouter, status
from starlette.responses import JSONResponse
from database.main import async_session_maker
from database.Address import AddressManager
from database.Carousel import CarouselManager
from database.City import CityManager
from database.Orders import OrderManager
from database.Post import PostManager
from database.Products import ProductManager
from database.Review import ReviewManager
from database.Setting import SettingManager
from database.Subscriber import SubscriberManager
from database.Template import TemplateManager
from database.User import UserManager
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


@router.post("/truncates")
async def truncates_all() -> JSONResponse:
    """
    Truncate all tables
    :return:
    """
    try:
        async with async_session_maker() as session:
            address_manager = AddressManager(session)
            query = await address_manager.truncate_posts_addresses()
            if query is False:
                raise Exception("Failed to truncate address")

            carousel_manager = CarouselManager(session)
            query = await carousel_manager.truncate_carousels_table()
            if query is False:
                raise Exception("Failed to truncate carousel")

            city_manager = CityManager(session)
            query = await city_manager.truncate_cities_table()
            if query is False:
                raise Exception("Failed to truncate city")

            orders_manager = OrderManager(session)
            query = await orders_manager.truncate_orders_table()
            if query is False:
                raise Exception("Failed to truncate orders")

            posts_manager = PostManager(session)
            query = await posts_manager.truncate_posts_table()
            if query is False:
                raise Exception("Failed to truncate posts")

            products_manager = ProductManager(session)
            query = await products_manager.truncate_products_table()
            if query is False:
                raise Exception("Failed to truncate products")

            review_manager = ReviewManager(session)
            query = await review_manager.truncate_reviews_table()
            if query is False:
                raise Exception("Failed to truncate reviews")

            settings_manager = SettingManager(session)
            query = await settings_manager.truncate_settings_table()
            if query is False:
                raise Exception("Failed to truncate settings")

            subscribers_manager = SubscriberManager(session)
            query = await subscribers_manager.truncate_subscribers_table()
            if query is False:
                raise Exception("Failed to truncate subscribers")

            templates_manager = TemplateManager(session)
            query = await templates_manager.truncate_templates_table()
            if query is False:
                raise Exception("Failed to truncate templates")

            users_manager = UserManager(session)
            query = await users_manager.truncate_users_table()
            if query is False:
                raise Exception("Failed to truncate users")
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": None,
                    "error": None
                }
            )
    except Exception as e:
        logging.exception(str(e))
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": str(e)
            }
        )
