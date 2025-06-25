import logging

from fastapi import APIRouter, Request
from starlette.responses import JSONResponse
from database.Orders import OrderManager
from database.main import async_session_maker

router = APIRouter()


@router.post("/get_orders_user")
async def get_orders_user(request: Request) -> JSONResponse:
    """
    Get orders user
    :param request:
    :return:
    """
    try:
        user_id = request.cookies.get("user_id")
        if user_id is None:
            return JSONResponse(
                status_code=200,
                content={"success": True, "data": None, "error": None}
            )

        async with async_session_maker() as session:
            order_manager = OrderManager(session)
            orders = await order_manager.get_orders_user(int(user_id))

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": {"orders": orders},
                "error": None
            }
        )

    except Exception as e:
        logging.exception(f"get_orders_user failed: {e}")
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "data": None,
                "error": "Failed to fetch orders"
            }
        )
