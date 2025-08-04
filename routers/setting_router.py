"""
Router module for managing user setting-related endpoints.
Includes operations for listing, creating, updating, and deleting setting.
"""
import logging

from fastapi import APIRouter, status, Request, HTTPException
from starlette.responses import JSONResponse
from faker import Faker
from database import (main, Address, City, Carousel, Orders, Post,
                      Products, Review, Setting, Subscriber, Template, User)
from helps.Middleware import is_admin
from models.SettingModel import Setting as SettingModel

router = APIRouter()


@router.post("/create")
async def create_setting(
        setting_: SettingModel,
        request: Request
) -> JSONResponse:
    """
    Create setting
    :param request:
    :param setting_:
    :return:
    """
    try:
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Missing user_id")
        admin = await is_admin(int(user_id))
        if not admin:
            raise HTTPException(status_code=403, detail="Permission denied")
        async with main.async_session_maker() as session:
            setting_manager = Setting.SettingManager(session)
            query = await setting_manager.create_setting(
                name=setting_.name,
                value=setting_.value,
            )
            if query is None:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to create setting"
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


@router.post("/auto_create")
async def auto_create_setting(request: Request) -> JSONResponse:
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
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Missing user_id")
        admin = await is_admin(int(user_id))
        if not admin:
            raise HTTPException(status_code=403, detail="Permission denied")
        async with main.async_session_maker() as session:
            setting_manager = Setting.SettingManager(session)
            for key, value in auto_fill.items():
                query = await setting_manager.create_setting(
                    name=key,
                    value=value,
                )
            if query is None:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to create setting"
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
async def update_setting(
        idx: int,
        setting_: SettingModel,
        request: Request
) -> JSONResponse:
    """
    Update setting
    :param request:
    :param idx:
    :param setting_:
    :return:
    """
    try:
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Missing user_id")
        admin = await is_admin(int(user_id))
        if not admin:
            raise HTTPException(status_code=403, detail="Permission denied")
        async with main.async_session_maker() as session:
            setting_manager = Setting.SettingManager(session)
            query = await setting_manager.update_setting(
                idx=idx,
                name=setting_.name,
                value=setting_.value,
            )
            if query is False:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to update setting"
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
async def get_setting(request: Request) -> JSONResponse:
    """
    Get settings
    :return:
    """
    try:
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Missing user_id")
        admin = await is_admin(int(user_id))
        if not admin:
            raise HTTPException(status_code=403, detail="Permission denied")
        async with main.async_session_maker() as session:
            setting_manager = Setting.SettingManager(session)
            query = await setting_manager.get_settings()
            if query is None:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to get setting"
                )
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


@router.get("/get/discount")
async def get_discount() -> JSONResponse:
    """
    Get discount
    :return:
    """
    try:
        async with main.async_session_maker() as session:
            setting_manager = Setting.SettingManager(session)
            query = await setting_manager.get_settings()
            if query is None:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to get setting"
                )
            dic = {}
            settings_ = [
                dic.update({setting.name: setting.value})
                for setting in query
                if setting.name in {"discount", "promotional"}
            ]
            if not settings_:
                raise HTTPException(
                    status_code=400,
                    detail="No matching settings found"
                )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": {"settings": dic},
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
async def delete_setting(idx: int, request: Request) -> JSONResponse:
    """
    Delete setting
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
            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )
        async with main.async_session_maker() as session:
            setting_manager = Setting.SettingManager(session)
            query = await setting_manager.delete_setting(idx=idx)
            if query is False:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to delete setting"
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


MANAGER_TRUNCATES = [
    (Address.AddressManager, "truncate_posts_addresses"),
    (Carousel.CarouselManager, "truncate_carousels_table"),
    (City.CityManager, "truncate_cities_table"),
    (Orders.OrderManager, "truncate_orders_table"),
    (Post.PostManager, "truncate_posts_table"),
    (Products.ProductManager, "truncate_products_table"),
    (Review.ReviewManager, "truncate_reviews_table"),
    (Setting.SettingManager, "truncate_settings_table"),
    (Subscriber.SubscriberManager, "truncate_subscribers_table"),
    (Template.TemplateManager, "truncate_templates_table"),
    (User.UserManager, "truncate_users_table")
]


async def truncate_all_managers(session):
    """
    Truncate all managers
    :param session:
    :return:
    """
    for manager_cls, method_name in MANAGER_TRUNCATES:
        manager = manager_cls(session)
        method = getattr(manager, method_name)
        success = await method()
        if not success:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to truncate via {method_name}"
            )


@router.post("/truncates")
async def truncates_all(request: Request) -> JSONResponse:
    """
    Truncate all managers
    :param request:
    :return:
    """
    try:
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Missing user_id")
        if not await is_admin(int(user_id)):
            raise HTTPException(status_code=403, detail="Permission denied")

        async with main.async_session_maker() as session:
            await truncate_all_managers(session)

        return JSONResponse(
            status_code=200,
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


async def set_address(faker: Faker) -> None:
    """
    Set fake address
    :param faker:
    :return:
    """
    async with main.async_session_maker() as session:
        address_manager = Address.AddressManager(session)
        for i in range(1, 101):
            await address_manager.create_address(
                name=faker.address(),
                city_id=i)


async def set_city(faker: Faker) -> None:
    """
    Set fake city
    :param faker:
    :return:
    """
    async with main.async_session_maker() as session:
        city_manager = City.CityManager(session)
        for _ in range(1, 11):
            for j in range(1, 11):
                await city_manager.create_city(
                    name=faker.city(),
                    post_id=j
                )


async def set_post_carousel(faker: Faker) -> None:
    """
    Set fake post and carousel
    :param faker:
    :return:
    """
    async with main.async_session_maker() as session:
        posts_manager = Post.PostManager(session)
        carousel_manager = Carousel.CarouselManager(session)
        for _ in range(1, 11):
            await posts_manager.create_post(faker.company())
            await carousel_manager.create_item(
                title=faker.name(),
                description=faker.text(),
                image=faker.name()
            )


async def set_product(faker: Faker) -> None:
    """
    Set fake product
    :param faker:
    :return:
    """
    async with main.async_session_maker() as session:
        products_manager = Products.ProductManager(session)
        for _ in range(1, 51):
            await products_manager.create_product(
                name=faker.name(),
                description=faker.text(),
                price=faker.random_int(),
                amount=faker.random_int()
            )


async def set_review(faker: Faker) -> None:
    """
    Set fake review
    :param faker:
    :return:
    """
    async with main.async_session_maker() as session:
        review_manager = Review.ReviewManager(session)
        for _ in range(1, 31):
            await review_manager.create_review(
                name=faker.first_name() + " " + faker.last_name(),
                text_=faker.text(),
                gender=int(faker.random_element(["0", "1"]))
            )


async def set_subscriber_tmp_users(faker: Faker) -> None:
    """
    Set fake subscriber_tmp_users
    :param faker:
    :return:
    """
    async with main.async_session_maker() as session:
        subscribers_manager = Subscriber.SubscriberManager(session)
        templates_manager = Template.TemplateManager(session)
        users_manager = User.UserManager(session)
        for _ in range(0, 20):
            await subscribers_manager.create_subscriber(
                email=faker.email(),
                hash_active=faker.text(max_nb_chars=15),
            )
            await templates_manager.create_template(
                title=faker.name(),
                header=faker.text(),
                body=faker.text()
            )
            await users_manager.create_user(
                username=faker.user_name(),
                email=faker.email(),
                phone=faker.phone_number(),
                password="qwertyQWERTY0!",
                hash_active_=faker.text(max_nb_chars=15)
            )


@router.post("/demo")
async def create_demo(request: Request) -> JSONResponse:
    """
    Create demo
    :return:
    """
    try:
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Missing user_id")
        admin = await is_admin(int(user_id))
        if not admin:
            raise HTTPException(status_code=403, detail="Permission denied")
        faker = Faker()
        await set_address(faker)
        await set_city(faker)
        await set_post_carousel(faker)
        await set_product(faker)
        await set_review(faker)
        await set_subscriber_tmp_users(faker)
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
