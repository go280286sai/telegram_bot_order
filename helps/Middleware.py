import logging

from database.User import UserManager
from database.main import async_session_maker


async def is_admin(idx: int) -> bool:
    try:
        async with async_session_maker() as session:
            user_manager = UserManager(session)
            user_ = await user_manager.get_user(idx)
            if user_ is None:
                raise Exception("User is not found")
            if user_.is_admin:
                return True
            else:
                return False
    except Exception as e:
        logging.exception(str(e))
        return False
