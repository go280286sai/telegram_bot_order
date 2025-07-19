import logging

from fastapi import APIRouter, status
from starlette.responses import JSONResponse
from database.main import async_session_maker
from database.Post import PostManager
from models.PostModel import Post

router = APIRouter()


@router.post("/create")
async def create_post(post_: Post) -> JSONResponse:
    """
    Create post
    :param post_:
    :return:
    """
    try:
        async with async_session_maker() as session:
            post_manager = PostManager(session)
            query = await post_manager.create_post(
                name=post_.name,
            )
            if query is False:
                raise Exception("Failed to create post")
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
                "error": str(e)
            }
        )


@router.post("/update/{idx}")
async def update_post(idx: int, post_: Post) -> JSONResponse:
    """
    Update post
    :param idx:
    :param post_:
    :return:
    """
    try:
        async with async_session_maker() as session:
            post_manager = PostManager(session)
            query = await post_manager.update_post(
                idx=idx,
                name=post_.name,
            )
            if query is False:
                raise Exception("Failed to update post")
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
                "error": "Failed to update post"
            }
        )


@router.get("/gets")
async def get_posts() -> JSONResponse:
    """
    Get posts
    :return:
    """
    try:
        async with async_session_maker() as session:
            post_manager = PostManager(session)
            query = await post_manager.get_posts()
            if query is None:
                raise Exception("Failed to get post")
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
    except Exception as e:
        logging.exception(f"Failed to fetch posts: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed to fetch posts"
            }
        )


@router.post("/delete/{idx}")
async def delete_post(idx: int) -> JSONResponse:
    """
    Delete post
    :param idx:
    :return:
    """
    try:
        async with async_session_maker() as session:
            post_manager = PostManager(session)
            query = await post_manager.delete_post(idx=idx)
            if query is False:
                raise Exception("Failed to delete post")
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": None,
                    "error": None
                }
            )
    except Exception as e:
        logging.exception(f"Failed to fetch post: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed to delete post"
            }
        )
