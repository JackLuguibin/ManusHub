import logging
import os
import sys
from datetime import datetime

from loguru import logger as _logger

from hub.config import DEFINE_LOGS_ROOT, DEFINE_PROJECT_ROOT

_std_level = logging.INFO
_file_level = logging.DEBUG
_output_file_flag = False
_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<cyan>{extra[relative_path]}</cyan>:<cyan>{name}</cyan>:"
    "<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)


def get_relative_path(record):
    file_path = record["file"].path
    return os.path.relpath(file_path, DEFINE_PROJECT_ROOT)


def enrich_with_relative_path(record):
    record["extra"]["relative_path"] = get_relative_path(record)
    return True


def settings(std_level=logging.INFO, file_level=logging.DEBUG, name: str = None, output: str = DEFINE_LOGS_ROOT):
    global _std_level, _file_level
    _std_level, _file_level = std_level, file_level

    current_date = datetime.now()
    formatted_date = current_date.strftime("%Y%m%d%H%M%S")
    log_name = name or (f"{name}_{formatted_date}" if name else formatted_date)

    _logger.remove()
    _logger.add(sys.stderr, level=_std_level, format=_format, filter=enrich_with_relative_path)
    if _output_file_flag:
        _logger.add(f"{output}/{log_name}.log", level=_file_level, format=_format)
    return _logger


logger = settings()
