import logging

from fastapi import APIRouter, status
from starlette.responses import JSONResponse

from database.User import UserManager
from database.main import async_session_maker
from database.Template import TemplateManager
from helps.emails import send_emails
from models.TemplateModel import Template

router = APIRouter()


@router.post("/create")
async def create_template(tmp: Template) -> JSONResponse:
    """
    Create template
    :param tmp:
    :return:
    """
    try:
        async with async_session_maker() as session:
            post_manager = TemplateManager(session)
            query = await post_manager.create_template(
                header=tmp.header,
                title=tmp.title,
                body=tmp.body
            )
            if query is False:
                raise Exception("Failed to create template")
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
                "error": "Failed to create template"
            }
        )


@router.post("/update/{idx}")
async def update_template(idx: int, tmp: Template) -> JSONResponse:
    """
    Update template
    :param idx:
    :param tmp:
    :return:
    """
    try:
        async with async_session_maker() as session:
            tmp_manager = TemplateManager(session)
            query = await tmp_manager.update_template(
                idx=idx,
                header=tmp.header,
                title=tmp.title,
                body=tmp.body
            )
            if query is False:
                raise Exception("Failed to update template")
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
                "error": "Failed to update template"
            }
        )


@router.get("/gets")
async def gets_templates() -> JSONResponse:
    """
    Get all templates.
    :return:
    """
    try:
        async with async_session_maker() as session:
            tmp_manager = TemplateManager(session)
            query = await tmp_manager.get_templates()
            if query is None:
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        "success": True,
                        "data": None,
                        "error": None
                    }
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
    except Exception as e:
        logging.exception(f"Failed to fetch templates: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed to fetch templates"
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
        async with async_session_maker() as session:
            tmp_manager = TemplateManager(session)
            query = await tmp_manager.get_template(idx=idx)
            if query is None:
                raise Exception("No templates")
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
    except Exception as e:
        logging.exception(f"Failed to fetch templates: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed to fetch templates"
            }
        )


@router.post("/delete/{idx}")
async def delete_template(idx: int) -> JSONResponse:
    """
    Delete template
    :param idx:
    :return:
    """
    try:
        async with async_session_maker() as session:
            tmp_manager = TemplateManager(session)
            query = await tmp_manager.delete_template(idx=idx)
            if query is False:
                raise Exception("Failed to delete template")
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": None,
                    "error": None
                }
            )
    except Exception as e:
        logging.exception(f"Failed delete template: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed to delete template"
            }
        )


@router.post("/send_users/{idx}")
async def send_users(idx: int) -> JSONResponse:
    """
    Send users message
    :param idx:
    :return:
    """
    try:
        async with async_session_maker() as session:
            tmp_manager = TemplateManager(session)
            tmp = await tmp_manager.get_template(idx=idx)
            user_manager = UserManager(session)
            users = await user_manager.get_users()
            if tmp is False or tmp is None:
                raise Exception("Failed to get template")
            if users is None:
                raise Exception("Failed to get users")
            for user in users:
                await send_emails(
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
    except Exception as e:
        logging.exception(f"Failed send users: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed send users"
            }
        )
