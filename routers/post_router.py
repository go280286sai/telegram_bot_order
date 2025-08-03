"""
Router module for managing post frontend-related endpoints.
Includes operations for listing, creating, updating, and deleting post.
"""
import logging

from fastapi import APIRouter, status, Request, HTTPException
from starlette.responses import JSONResponse
from database import main, Post
from helps.Middleware import is_admin
from models.PostModel import Post as PostModel

router = APIRouter()


@router.post("/create")
async def create_post(post_: PostModel, request: Request) -> JSONResponse:
    """
    Create post
    :param request:
    :param post_:
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
            post_manager = Post.PostManager(session)
            query = await post_manager.create_post(
                name=post_.name,
            )
            if query is False:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to create post"
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
async def update_post(
        idx: int,
        post_: PostModel,
        request: Request
) -> JSONResponse:
    """
    Update post
    :param request:
    :param idx:
    :param post_:
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
            post_manager = Post.PostManager(session)
            query = await post_manager.update_post(
                idx=idx,
                name=post_.name,
            )
            if query is False:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to update post"
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
async def get_posts() -> JSONResponse:
    """
    Get posts
    :return:
    """
    try:
        async with main.async_session_maker() as session:
            post_manager = Post.PostManager(session)
            query = await post_manager.get_posts()
            if query is None:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to create carousel"
                )
            posts_ = [
                {
                    "id": p.id,
                    "name": p.name,
                } for p in query
            ]
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": {"posts": posts_},
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
async def delete_post(idx: int, request: Request) -> JSONResponse:
    """
    Delete post
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
        async with main.async_session_maker() as session:
            post_manager = Post.PostManager(session)
            query = await post_manager.delete_post(idx=idx)
            if query is False:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to delete post"
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
