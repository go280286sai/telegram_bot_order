import logging
from fastapi import APIRouter
from models.LogsModel import Logs

router = APIRouter()


@router.post("/create")
async def logs(log: Logs):
    """
    Logs created.
    :param log:
    :return:
    """
    try:
        logging.info(f"{log.level} - {log.name} - {log.message}")
        return {
            "success": True,
            "data": None,
            "error": None
        }
    except Exception as e:
        logging.exception("Exception occurred")
        return {
            "success": False,
            "data": None,
            "error": f"Error write log str({e})"
        }
