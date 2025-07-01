import logging
from fastapi import APIRouter, Request, status
from starlette.responses import JSONResponse
from database.User import UserManager
from database.main import async_session_maker
from models.UserModel import User, Login, UpdateUser

router = APIRouter()


@router.post("/register")
async def register(user: User) -> JSONResponse:
    """
    Register a new user.
    :param user:
    :return:
    """
    try:
        async with async_session_maker() as session:
            user_manager = UserManager(session)
            new_user = await user_manager.create_user(
                username=user.username,
                password=user.password,
                phone=user.phone,
                email=user.email
            )
            if new_user is None:
                raise Exception("Failed to create user")
            response = JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": None,
                    "error": None
                }
            )
            response.set_cookie(
                key="user_id",
                value=str(new_user.id),
                httponly=True
            )
            return response
    except Exception as e:
        logging.exception(f"Registration failed {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "User already exists"
            }
        )


@router.post("/is_auth")
async def is_auth(request: Request) -> JSONResponse:
    """
    Check if user is authenticated.
    :param request:
    :return:
    """
    try:
        user_id = request.cookies.get("user_id")
        if user_id is None:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": None,
                    "error": None
                }
            )

        async with async_session_maker() as session:
            user_manager = UserManager(session)
            user = await user_manager.get_user(int(user_id))
            if user:
                user_data = {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "phone": user.phone,
                    "status": user.status
                }
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        "success": True,
                        "data": user_data,
                        "error": None
                    }
                )
            else:
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
                "error": "User does not exist"
            }
        )


@router.post("/login")
async def login(user: Login) -> JSONResponse:
    """
    Login a new user.
    :param user:
    :return:
    """
    try:
        async with async_session_maker() as session:
            user_manager = UserManager(session)
            new_user = await user_manager.get_user_by_username(
                user.username,
                user.password
            )
            if new_user is None:
                raise Exception("User does not exist")
            response = JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": {"user_id": new_user.id},
                    "error": None
                }
            )
            response.set_cookie(
                key="user_id",
                value=str(new_user.id),
                httponly=True
            )
            return response
    except Exception as e:
        logging.exception(f"Login failed {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": "Invalid credentials"
            }
        )


@router.post("/logout")
async def logout() -> JSONResponse:
    try:
        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "data": True,
                "error": None
            }
        )
        response.set_cookie(
            key="user_id",
            value="",
            max_age=0,
            httponly=True
        )
        return response
    except Exception as e:
        logging.exception(f"Logout failed {str(e)}")
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "data": False,
                "error": "Failed to logout"
            }
        )


@router.post("/update_profile")
async def update_profile(user: UpdateUser) -> JSONResponse:
    """
    Update profile data.
    :param user:
    :return:
    """
    try:
        async with async_session_maker() as session:
            user_manager = UserManager(session)
            await user_manager.update_user(
                password=user.password,
                idx=user.idx
            )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": True,
                    "error": None
                }
            )
    except Exception as e:
        logging.exception(f"Profile update failed {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": False,
                "error": "Failed to update user"
            }
        )


@router.post("/delete/{idx}")
async def user_delete(idx: int) -> JSONResponse:
    """
    Delete user's data.'
    :param idx:
    :return:
    """
    try:
        async with async_session_maker() as session:
            user_manager = UserManager(session)
            await user_manager.delete_user(idx)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": None,
                    "error": None
                }
            )
    except Exception as e:
        logging.exception(f"User delete failed {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": False,
                "error": "Failed to delete user"
            }
        )
