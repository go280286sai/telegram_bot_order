"""
Router module for managing user logs-related endpoints.
Includes operations for creating log entries and updating log entries.
"""

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
        logging.info("%s - %s - %s", log, log.name, log.message)
        return {
            "success": True,
            "data": None,
            "error": None
        }
    except ValueError as e:
        logging.exception("Exception occurred")
        return {
            "success": False,
            "data": None,
            "error": f"Error write log str({e})"
        }
