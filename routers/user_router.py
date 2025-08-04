"""
Router module for managing user related endpoints.
Includes operations for creating, updating, and deleting user.
"""
import logging
from fastapi import (APIRouter, Request,
                     status, BackgroundTasks, HTTPException)
from starlette.responses import JSONResponse, HTMLResponse
from database import main, User
from helps import emails, helper, Middleware
from models import RecoveryModel, UserModel, TemplateModel

router = APIRouter()


@router.post("/register")
async def register(
        user: UserModel.User,
        request: Request,
        background_task: BackgroundTasks
) -> JSONResponse:
    """
    Register a new user.
    :param background_task:
    :param request:
    :param user:
    :return:
    """
    async with main.async_session_maker() as session:
        try:
            if not all([helper.is_valid_email(user.email),
                        helper.validate_password(user.password)]):
                raise HTTPException(
                    status_code=422,
                    detail="Missing email or password"
                )
            user_manager = User.UserManager(session)
            new_user = await user_manager.create_user(
                username=user.username,
                password=user.password,
                phone=user.phone,
                email=user.email,
                hash_active_=helper.generate_transaction()
            )
            if new_user is None:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to create user"
                )
            background_task.add_task(
                emails.register_user_confirm, email=new_user["email"],
                idx=int(new_user["id"]), hash_active=new_user["hashed_active"]
            )
            request.session["user_id"] = str(new_user["id"])
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": {"user": new_user},
                    "error": False
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


@router.post("/is_auth")
async def is_auth(request: Request) -> JSONResponse:
    """
    Check if user is authenticated.
    :param request:
    :return:
    """
    try:
        async with main.async_session_maker() as session:
            user_id = request.session.get("user_id")
            if user_id is None:
                raise HTTPException(
                    status_code=401,
                    detail="Missing user_id"
                )
            user_manager = User.UserManager(session)
            user = await user_manager.get_user(int(user_id))
            if user is None:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to get user"
                )
            user_data = {
                "id": user['id'],
                "username": user['username'],
                "email": user['email'],
                "phone": user['phone'],
                "status": user['status'],
                "is_admin": user['is_admin'],
                "first_name": user['first_name'],
                "last_name": user['last_name'],
                "bonus": user['bonus']}
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": user_data,
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


@router.post("/login")
async def login(user: UserModel.Login, request: Request) -> JSONResponse:
    """
    Login a new user.
    :param request:
    :param user:
    :return:
    """
    try:
        async with main.async_session_maker() as session:
            user_manager = User.UserManager(session)
            new_user = await user_manager.get_user_by_username(
                user.username,
                user.password
            )
            if new_user is None:
                raise HTTPException(
                    status_code=400,
                    detail="User does not exist"
                )
            request.session["user_id"] = str(new_user.id)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": {"user_id": new_user.id},
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


@router.post("/logout")
async def logout(request: Request) -> JSONResponse:
    """
    Logout a user.
    :param request:
    :return:
    """
    try:
        request.session.clear()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "data": True,
                "error": None
            }
        )
    except ValueError as e:
        logging.exception(e)
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "data": False,
                "error": str(e)
            }
        )


@router.post("/update_profile")
async def update_profile(
        user: UserModel.UpdateUser,
        request: Request
) -> JSONResponse:
    """
    Update profile data.
    :param request:
    :param user:
    :return:
    """
    try:
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Missing user_id")
        password = helper.validate_password(user.password)
        if password is False:
            raise HTTPException(status_code=400, detail="Invalid password")
        async with main.async_session_maker() as session:
            user_manager = User.UserManager(session)
            result = await user_manager.update_user(
                password=user.password,
                idx=int(user_id)
            )
            if not result:
                raise HTTPException(
                    status_code=400,
                    detail="User update error"
                )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": True,
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


@router.post("/add_contact_profile")
async def add_contact_profile(
        user: UserModel.AddName,
        request: Request
) -> JSONResponse:
    """
    Update profile first name and last name.
    :param request:
    :param user:
    :return:
    """
    try:
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Missing user_id")
        async with main.async_session_maker() as session:
            user_manager = User.UserManager(session)
            result = await user_manager.update_user_name(
                idx=int(user_id),
                first_name=user.first_name,
                last_name=user.last_name
            )
            if not result:
                raise HTTPException(
                    status_code=400,
                    detail="User does not exist"
                )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": True,
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
async def user_delete(idx: int, request: Request) -> JSONResponse:
    """
    Delete user's data.'
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
            user_manager = User.UserManager(session)
            result = await user_manager.delete_user(idx)
            if not result:
                raise HTTPException(
                    status_code=400,
                    detail="User does not exist"
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


@router.get("/confirm/{idx}/{token}", response_model=None)
async def user_confirm(idx: int, token: str) -> HTMLResponse | JSONResponse:
    """
    Confirm user's data.'
    :param idx:
    :param token:
    :return:
    """
    try:
        async with main.async_session_maker() as session:
            user_manager = User.UserManager(session)
            hash_active = str(token)
            idx = int(idx)
            result = await user_manager.get_user(idx=idx)
            if result is None:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to confirm register"
                )
            if hash_active != result["hashed_active"]:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to confirm register"
                )
            await user_manager.set_status(user_id=idx, status=1)
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


@router.post("/recovery")
async def recovery(
        recovery_: RecoveryModel.Recovery,
        background_task: BackgroundTasks
) -> JSONResponse:
    """
    Recover user's data.'
    :param background_task:
    :param recovery_:
    :return:
    """
    try:
        async with main.async_session_maker() as session:
            if not helper.is_valid_email(recovery_.email):
                raise HTTPException(status_code=422, detail="Missing email")
            user_manager = User.UserManager(session)
            new_user = await user_manager.get_user_by_username_email(
                recovery_.username,
                recovery_.email
            )
            if new_user is None:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid email error"
                )
            recovery_pass = await user_manager.reset_password(new_user.id)
            if recovery_pass is None:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid email error"
                )
            background_task.add_task(
                emails.send_emails,
                header="Recovery email",
                title="Recovery email",
                body=f"Your recovery password is {recovery_pass}",
                idx=new_user.id,
                email=new_user.email,
                hash_active=new_user.hashed_active,
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
        logging.exception(e)
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "success": False,
                "data": None,
                "error": e
            }
        )
    except Middleware.DatabaseException as e:
        logging.exception(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "data": None,
                "error": e
            }
        )


@router.post("/gets")
async def gets_users(request: Request) -> JSONResponse:
    """
    Get all user's data.'
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
            user_manager = User.UserManager(session)
            users = await user_manager.get_users()
            if users is None:
                raise HTTPException(
                    status_code=400,
                    detail="Fetching users failed"
                )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": {"users": users},
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
async def get_user(idx: int, request: Request) -> JSONResponse:
    """
    Get user data.
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
            user_manager = User.UserManager(session)
            users = await user_manager.get_user(idx=idx)
            if users is None:
                raise HTTPException(
                    status_code=400,
                    detail="Fetching user failed"
                )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "data": users,
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


@router.post("/update")
async def update_users(
        users_: UserModel.UpdateUsers,
        request: Request
) -> JSONResponse:
    """
    Update users
    :return:
    """
    try:
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Missing user_id"
            )
        admin = await Middleware.is_admin(int(user_id))
        if not admin:
            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )
        async with main.async_session_maker() as session:
            user_manager = User.UserManager(session)
            users = await user_manager.update_users(
                idx=int(user_id),
                username=users_.username,
                email=users_.email,
                phone=users_.phone,
                comments="" if len(users_.comments) == 0 else users_.comments,
                first_name=users_.first_name,
                last_name=users_.last_name
            )
            if users is False:
                raise HTTPException(
                    status_code=400,
                    detail="Fetching users failed"
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


@router.post("/set_status/{idx}/{stat}")
async def set_status_user(
        idx: int, stat: int,
        request: Request
) -> JSONResponse:
    """
    Set status users
    :param idx:
    :param stat:
    :param request:
    :return:
    """
    try:
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Missing user_id"
            )
        admin = await Middleware.is_admin(int(user_id))
        if not admin:
            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )
        async with main.async_session_maker() as session:
            user_manager = User.UserManager(session)
            users = await user_manager.set_status(
                user_id=int(idx), status=int(stat))
            if not users:
                raise HTTPException(
                    status_code=400,
                    detail="Fetching users failed"
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


@router.post("/set_status_admin/{idx}/{stat}")
async def set_status_admin(
        idx: int, stat: int,
        request: Request
) -> JSONResponse:
    """
    Set status users
    :param idx:
    :param stat:
    :param request:
    :return:
    """
    try:
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Missing user_id"
            )
        admin = await Middleware.is_admin(int(user_id))
        if not admin:
            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )
        async with main.async_session_maker() as session:
            user_manager = User.UserManager(session)
            users = await user_manager.set_admin(
                user_id=int(idx), status=int(stat))
            if not users:
                raise HTTPException(
                    status_code=400,
                    detail="Fetching users failed"
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


@router.post("/send_email/{idx}/{email}")
async def send_email_user(
        tmp: TemplateModel.Template,
        idx: int,
        email: str,
        request: Request,
        background_task: BackgroundTasks
) -> JSONResponse:
    """
    Send email
    :param background_task:
    :param tmp:
    :param idx:
    :param request:
    :param email:
    :return:
    """
    try:
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Missing user_id")
        admin = await Middleware.is_admin(int(user_id))
        if not admin:
            raise HTTPException(status_code=403, detail="Permission denied")
        background_task.add_task(
            emails.send_emails,
            header=tmp.header,
            title=tmp.title,
            body=tmp.body,
            idx=int(idx),
            email=email,
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


@router.post("/delete/{idx}")
async def user_delete_id(idx: int, request: Request) -> JSONResponse:
    """
    Set status users
    :param idx:
    :param request:
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
            user_manager = User.UserManager(session)
            users = await user_manager.delete_user(
                idx=int(idx)
            )
            if users is False:
                raise HTTPException(
                    status_code=400,
                    detail="Deleting users failed"
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


@router.post("/delete_user")
async def delete_user(
        request: Request,
        background_task: BackgroundTasks
) -> JSONResponse:
    """
    Send email for delete user
    :return:
    """
    try:
        user_id = request.session.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Missing user_id")
        async with main.async_session_maker() as session:
            user_manager = User.UserManager(session)
            user_hashed_active = helper.generate_transaction()
            delete_users = await user_manager.set_hashed_active_for_delete(
                idx=str(user_id), hashed_active=user_hashed_active)
            if delete_users is None:
                raise HTTPException(status_code=400, detail="User not found")
            background_task.add_task(
                emails.delete_user_confirm, email=delete_users,
                idx=int(user_id), hash_active=user_hashed_active)
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


@router.get("/delete_confirm/{idx}/{token}", response_model=None)
async def user_delete_confirm(
        idx: int, token: str
) -> HTMLResponse | JSONResponse:
    """
    Send email for delete user
    :param idx:
    :param token:
    :return:
    """
    try:
        hash_active = str(token)
        idx = int(idx)
        async with main.async_session_maker() as session:
            user_manager = User.UserManager(session)
            result = await user_manager.get_user(idx=idx)
            if result is None:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to confirm delete"
                )
            if hash_active != result['hashed_active']:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to confirm delete"
                )
            await user_manager.delete_user(idx=idx)
            return await emails.confirm_delete_user()

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
