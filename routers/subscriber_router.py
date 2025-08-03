"""
Router module for managing user subscriber-related endpoints.
Includes operations for listing, creating, updating, and deleting subscriber.
"""
import logging
from fastapi import APIRouter, status, BackgroundTasks, Request, HTTPException
from starlette.responses import JSONResponse
from database import main, Subscriber, Template
from helps import Middleware, helper, emails
from models.SubscriberModel import Subscriber as SubscriberModel

router = APIRouter()


@router.post("/create")
async def create_subscriber_route(
        sub: SubscriberModel,
        background_task: BackgroundTasks
):
    """
    Create subscriber route.
    :param sub:
    :param background_task:
    :return:
    """
    try:
        async with main.async_session_maker() as session:
            if not emails.is_valid_email(sub.email):
                raise HTTPException(status_code=401, detail="Missing email")
            subscriber_manager = Subscriber.SubscriberManager(session)
            hash_active = helper.generate_transaction()
            result = await subscriber_manager.create_subscriber(
                email=sub.email,
                hash_active=hash_active
            )
            if not result:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to create subscriber"
                )
            background_task.add_task(
                emails.create_subscriber_email,
                idx=int(result.id),
                email=sub.email,
                hash_active=hash_active
            )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": None,
                    "error": None
                })
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


@router.get("/confirm/{idx}/{token}")
async def confirm_subscriber_route(idx: int, token: str):
    """
    Confirm subscriber route.
    :param idx:
    :param token:
    :return:
    """
    try:
        async with main.async_session_maker() as session:
            subscriber_manager = Subscriber.SubscriberManager(session)
            hash_active = str(token)
            result = await subscriber_manager.set_active_subscriber(
                idx=idx,
                hash_active=hash_active
            )
            if result is False:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to confirm subscriber"
                )
            return await emails.confirm_email()
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


@router.get("/destroy/{idx}/{token}")
async def destroy_route(idx: int, token: str):
    """
    Destroy subscriber route.
    :param idx:
    :param token:
    :return:
    """
    try:
        async with main.async_session_maker() as session:
            subscriber_manager = Subscriber.SubscriberManager(session)
            hash_destroy = str(token)
            destroy = await subscriber_manager.set_destroy_subscriber(
                idx=idx,
                hash_destroy=hash_destroy
            )
            if destroy is False:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to destroy subscriber"
                )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": None,
                    "error": None
                })
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


@router.post("/send_email/{idx}")
async def send_email_route(idx: int):
    """
    Send email route.
    :param idx:
    :return:
    """
    async with main.async_session_maker() as session:
        idx = int(idx)
        tmp_manager = Template.TemplateManager(session)
        await tmp_manager.get_template(idx=idx)


@router.post("/send_subscribers/{idx}")
async def send_users(
        idx: int,
        background_tasks: BackgroundTasks,
        request: Request
) -> JSONResponse:
    """
    Send users message
    :param request:
    :param background_tasks:
    :param idx:
    :return:
    """
    try:
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Missing user_id")
        admin = await Middleware.is_admin(int(user_id))
        if not admin:
            raise HTTPException(status_code=403, detail="Permission denied")
        async with main.async_session_maker() as session:
            tmp_manager = Template.TemplateManager(session)
            tmp = await tmp_manager.get_template(idx=idx)
            subscriber_manager = Subscriber.SubscriberManager(session)
            subscribers = await subscriber_manager.get_subscribers()
            if tmp is None:
                raise HTTPException(
                    status_code=400,
                    detail="Template not found"
                )
            if subscribers is None:
                raise HTTPException(
                    status_code=400,
                    detail="No subscribers available"
                )

            for subscriber in subscribers:
                background_tasks.add_task(
                    emails.send_emails,
                    header=tmp.header,
                    title=tmp.title,
                    body=tmp.body,
                    idx=subscriber['id'],
                    email=subscriber['email'],
                    hash_active="",
                    footer=True)

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
