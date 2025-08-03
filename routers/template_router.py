"""
Router module for managing user template-related endpoints.
Includes operations for listing, creating, updating, and deleting template.
"""
import logging

from fastapi import APIRouter, status, Request, HTTPException, BackgroundTasks
from starlette.responses import JSONResponse
from database import main, User, Template
from helps import Middleware, emails
from models.TemplateModel import Template as TemplateModel

router = APIRouter()


@router.post("/create")
async def create_template(
        tmp: TemplateModel,
        request: Request
) -> JSONResponse:
    """
    Create template
    :param request:
    :param tmp:
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
            post_manager = Template.TemplateManager(session)
            query = await post_manager.create_template(
                header=tmp.header,
                title=tmp.title,
                body=tmp.body
            )
            if query is False:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to create template"
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
async def update_template(
        idx: int,
        tmp: TemplateModel,
        request: Request
) -> JSONResponse:
    """
    Update template
    :param request:
    :param idx:
    :param tmp:
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
            query = await tmp_manager.update_template(
                idx=idx,
                header=tmp.header,
                title=tmp.title,
                body=tmp.body
            )
            if query is False:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to update template"
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
async def gets_templates() -> JSONResponse:
    """
    Get all templates.
    :return:
    """
    try:
        async with main.async_session_maker() as session:
            tmp_manager = Template.TemplateManager(session)
            query = await tmp_manager.get_templates()
            if query is None:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to get templates"
                )
            tmp_ = [
                {
                    "id": p.id,
                    "header": p.header,
                    "title": p.title,
                    "body": p.body,
                } for p in query
            ]
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": {"templates": tmp_},
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


@router.post("/get/{idx}")
async def get_template(idx: int) -> JSONResponse:
    """
    Get template.
    :param idx:
    :return:
    """
    try:
        async with main.async_session_maker() as session:
            tmp_manager = Template.TemplateManager(session)
            query = await tmp_manager.get_template(idx=idx)
            if query is None:
                raise HTTPException(status_code=400, detail="No templates")
            tmp_ = [
                {
                    "id": query.id,
                    "header": query.header,
                    "title": query.title,
                    "body": query.body,
                }
            ]

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": {"templates": tmp_},
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
async def delete_template(idx: int, request: Request) -> JSONResponse:
    """
    Delete template
    :param request:
    :param idx:
    :return:
    """
    try:
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Missing user_id")
        admin = await Middleware.is_admin(int(user_id))
        if not admin:
            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )
        async with main.async_session_maker() as session:
            tmp_manager = Template.TemplateManager(session)
            query = await tmp_manager.delete_template(idx=idx)
            if query is False:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to delete template"
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


@router.post("/send_users/{idx}")
async def send_users(
        idx: int,
        request: Request,
        background_task: BackgroundTasks
) -> JSONResponse:
    """
    Send users message
    :param background_task:
    :param request:
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
            user_manager = User.UserManager(session)
            users = await user_manager.get_users()
            if tmp is None:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to get template"
                )
            if users is None:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to get users"
                )
            for user in users:
                background_task.add_task(
                    emails.send_emails,
                    header=tmp.header,
                    title=tmp.title,
                    body=tmp.body,
                    idx=user['id'],
                    email=user['email'],
                    hash_active="",
                    footer=False
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
