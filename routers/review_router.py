"""
Router module for managing user review-related endpoints.
Includes operations for listing, creating, updating, and deleting review.
"""
import logging

from fastapi import APIRouter, status, Request, HTTPException
from starlette.responses import JSONResponse
from database import main, Review
from helps.Middleware import is_admin
from models.ReviewModel import Review as ReviewModel

router = APIRouter()


@router.post("/create")
async def review_create(item: ReviewModel, request: Request) -> JSONResponse:
    """
    Create a new review.
    :param request:
    :param item:
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
            review_manager = Review.ReviewManager(session)
            query = await review_manager.create_review(
                name=item.name,
                text_=item.text,
                gender=item.gender,
            )
            if query is False:
                raise HTTPException(
                    status_code=400,
                    detail="Error creating review"
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
async def review_update(
        idx: int,
        item: ReviewModel,
        request: Request
) -> JSONResponse:
    """
    Update an existing review.
    :param request:
    :param idx:
    :param item:
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
            product_manager = Review.ReviewManager(session)
            query = await product_manager.update_review(
                idx=idx,
                name=item.name,
                text_=item.text,
                gender=item.gender
            )
            if query is False:
                raise HTTPException(
                    status_code=400,
                    detail="Error updating review"
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


@router.get("/reviews")
async def reviews() -> JSONResponse:
    """
    Get all reviews.
    :return:
    """
    try:
        async with main.async_session_maker() as session:
            product_manager = Review.ReviewManager(session)
            query = await product_manager.get_reviews()
            if query is None:
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        "success": False,
                        "data": None,
                        "error": "No reviews"
                    }
                )
            reviews_ = [
                {
                    "id": p.id,
                    "name": p.name,
                    "text": p.text,
                    "gender": p.gender,
                } for p in query
            ]

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": {"reviews": reviews_},
                    "error": None
                }
            )
    except ValueError as e:
        logging.exception(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": str(e)
            }
        )


@router.post("/delete/{idx}")
async def review_delete(idx: int, request: Request) -> JSONResponse:
    """
    Delete an existing review.
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
            product_manager = Review.ReviewManager(session)
            query = await product_manager.delete_review(idx=idx)
            if query is False:
                raise HTTPException(
                    status_code=400,
                    detail="Error deleting review"
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
