import logging

from fastapi import APIRouter, status
from database.Review import ReviewManager
from database.main import async_session_maker
from starlette.responses import JSONResponse
from models.ReviewModel import Review

router = APIRouter()


@router.post("/create")
async def review_create(item: Review) -> JSONResponse:
    """
    Create a new review.
    :param item:
    :return:
    """
    try:
        async with async_session_maker() as session:
            review_manager = ReviewManager(session)
            query = await review_manager.create_review(
                name=item.name,
                text=item.text,
                gender=item.gender,
            )
            if query is False:
                raise Exception("Error creating review")

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": None,
                    "error": None
                }
            )
    except Exception as e:
        logging.exception(f"Error creating review: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Error creating review"
            }
        )


@router.post("/update/{idx}")
async def review_update(idx: int, item: Review) -> JSONResponse:
    """
    Update an existing review.
    :param idx:
    :param item:
    :return:
    """
    try:
        async with async_session_maker() as session:
            product_manager = ReviewManager(session)
            query = await product_manager.update_review(
                idx=idx,
                name=item.name,
                text=item.text,
                gender=item.gender
            )
            if query is False:
                raise Exception("Error updating review")
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": None,
                    "error": None
                }
            )
    except Exception as e:
        logging.exception(f"Error updating review: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Error updating review"
            }
        )


@router.get("/reviews")
async def reviews() -> JSONResponse:
    """
    Get all reviews.
    :return:
    """
    try:
        async with async_session_maker() as session:
            product_manager = ReviewManager(session)
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
    except Exception as e:
        logging.exception(f"Failed to fetch reviews: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed to fetch reviews"
            }
        )


@router.post("/delete/{idx}")
async def review_delete(idx: int) -> JSONResponse:
    """
    Delete an existing review.
    :param idx:
    :return:
    """
    try:
        async with async_session_maker() as session:
            product_manager = ReviewManager(session)
            query = await product_manager.delete_review(idx=idx)
            if query is False:
                raise Exception("Error deleting review")

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": None,
                    "error": None
                }
            )
    except Exception as e:
        logging.exception(f"Failed to fetch reviews: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Failed to fetch reviews"
            }
        )
