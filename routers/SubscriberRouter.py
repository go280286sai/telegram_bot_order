import logging
from fastapi import APIRouter, status
from starlette.responses import JSONResponse
from database.main import async_session_maker
from database.Subscriber import SubscriberManager
from database.Template import TemplateManager
from models.SubscriberModel import Subscriber
from helps.help import is_valid_email, generate_transaction
from helps.emails import create_subscriber_email, confirm_email

router = APIRouter()


@router.post("/create")
async def create_subscriber_route(sub: Subscriber):
    try:
        async with async_session_maker() as session:
            if not is_valid_email(sub.email):
                return JSONResponse(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    content={
                        "success": False,
                        "data": None,
                        "error": "Invalid email format"
                    }
                )
            subscriber_manager = SubscriberManager(session)
            hash_active = generate_transaction()
            result = await subscriber_manager.create_subscriber(
                email=sub.email,
                hash_active=hash_active
            )
            if not result:
                raise Exception("Failed to create subscriber")
            send_email = await create_subscriber_email(
                idx=int(result.id),
                email=sub.email,
                hash_active=hash_active
            )
            if send_email is None:
                raise Exception("Failed to create subscriber")

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": None,
                    "error": None
                })
    except Exception as e:
        logging.exception(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed to confirm subscriber"
            }
        )


@router.get("/confirm/{idx}/{token}")
async def confirm_subscriber_route(idx: int, token: str):
    try:
        async with async_session_maker() as session:
            subscriber_manager = SubscriberManager(session)
            hash_active = str(token)
            result = await subscriber_manager.set_active_subscriber(
                idx=idx,
                hash_active=hash_active
            )
            if result is False:
                raise Exception("Failed to confirm subscriber")

            return await confirm_email()

    except Exception as e:
        logging.exception(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed add subscriber"
            }
        )


@router.get("/destroy/{idx}/{token}")
async def destroy_route(idx: int, token: str):
    try:
        async with async_session_maker() as session:
            subscriber_manager = SubscriberManager(session)
            hash_destroy = str(token)
            await subscriber_manager.set_destroy_subscriber(
                idx=idx,
                hash_destroy=hash_destroy
            )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": None,
                    "error": None
                })
    except Exception as e:
        logging.exception(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed add subscriber"
            }
        )


@router.post("/send_email/{idx}")
async def send_email_route(idx: int):
    async with async_session_maker() as session:
        idx = int(idx)
        tmp_manager = TemplateManager(session)
        await tmp_manager.get_template(idx=idx)
