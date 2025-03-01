import logging
import os
from logging.handlers import RotatingFileHandler

from colorama import Fore

from .LogConsoleFormatter import LogConsoleFormatter
from .LogUtility import log_and_raise

_DATE_FORMAT_STR = "%Y-%m-%d %H:%M:%S"

_FILE_FORMAT_STR = "[%(asctime)s] [%(levelname)-8s] [%(name)s]: %(message)s"
_FILE_MODE = "a"
_FILE_MAX_BYTES = 1024 * 1024
_FILE_BACKUP_COUNT = 4
_FILE_ENCODING = "utf-8"

_CONSOLE_FORMAT_STR = "[{asctime}] [{levelname}] [{name}]: {message}"
_COLOR_NAME = Fore.CYAN
_COLOR_MESSAGE = Fore.RESET

_ENABLE_FILE_LOGGING = True
_ENABLE_CONSOLE_LOGGING = True

_ALLOWED_LEVELS = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]


def get_logger(
    name: str,
    level: int | str = logging.INFO,
    *,
    date_format_str: str = _DATE_FORMAT_STR,
    file_format_str: str = _FILE_FORMAT_STR,
    file_path: str = None,
    file_mode: str = _FILE_MODE,
    file_max_bytes: int = _FILE_MAX_BYTES,
    file_backup_count: int = _FILE_BACKUP_COUNT,
    file_encoding: str = _FILE_ENCODING,
    console_format_str: str = _CONSOLE_FORMAT_STR,
    console_color_name: str = _COLOR_NAME,
    console_color_message: str = _COLOR_MESSAGE,
    console_level_colors: dict[str, str] = None,
    enable_file_logging: bool = _ENABLE_FILE_LOGGING,
    enable_console_logging: bool = _ENABLE_CONSOLE_LOGGING,
) -> logging.Logger:
    """
    Creates and configures a logger with optional file and console handlers.

    Args:
        name (str): The name of the logger.
        level (int | str): The logging level (e.g., logging.INFO, "DEBUG"). Defaults to logging.INFO.
        date_format_str (str): The format string for dates. Defaults to _DATE_FORMAT_STR.
        file_format_str (str): The format string for file log entries. Defaults to _FILE_FORMAT_STR.
        file_path (str): The path to the log file. If None, file logging is disabled. Defaults to None.
        file_mode (str): The file mode. Defaults to _FILE_MODE ("a").
        file_max_bytes (int): The maximum size of the log file in bytes before rotating. Defaults to _FILE_MAX_BYTES.
        file_backup_count (int): The number of backup log files to keep. Defaults to _FILE_BACKUP_COUNT.
        file_encoding (str): The encoding of the log file. Defaults to _FILE_ENCODING.
        console_format_str (str): The format string for console log entries. Defaults to _CONSOLE_FORMAT_STR.
        console_color_name (str): The color for the logger name in console output. Defaults to Fore.RESET.
        console_color_message (str): The color for the message in console output. Defaults to Fore.RESET.
        console_level_colors (dict[str, str]): A dictionary mapping log levels to colors for console output. Defaults to LogConsoleFormatter.DEFAULT_LEVEL_COLORS.
        enable_file_logging (bool): Whether to enable file logging. Defaults to _ENABLE_FILE_LOGGING.
        enable_console_logging (bool): Whether to enable console logging. Defaults to _ENABLE_CONSOLE_LOGGING.

    Returns:
        logging.Logger: The configured logger.
    """

    if isinstance(level, str):
        level = logging.getLevelName(level.upper())
        if isinstance(level, int):
            if level not in _ALLOWED_LEVELS:
                log_and_raise(__name__, f"Logging level not allowed: {logging.getLevelName(level)}", ValueError)
        else:
            log_and_raise(__name__, f"Logging level not found: {level}", ValueError)
    elif isinstance(level, int):
        if level not in _ALLOWED_LEVELS:
            log_and_raise(__name__, f"Logging level not allowed: {logging.getLevelName(level)}", ValueError)
    else:
        log_and_raise(__name__, f"Logging level type not allowed: {type(level)}", TypeError)

    logger = logging.getLogger(name=name)
    logger.setLevel(level=level)

    if enable_file_logging and file_path:
        file_path = file_path if file_path.endswith(".log") else f"{file_path}.log"
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

        file_handler = RotatingFileHandler(
            filename=file_path,
            mode=file_mode,
            maxBytes=file_max_bytes,
            backupCount=file_backup_count,
            encoding=file_encoding,
        )
        file_formatter = logging.Formatter(
            fmt=file_format_str,
            datefmt=date_format_str,
        )
        file_handler.setFormatter(fmt=file_formatter)
        logger.addHandler(hdlr=file_handler)

    if enable_console_logging:
        console_handler = logging.StreamHandler()
        console_formatter = LogConsoleFormatter(
            fmt=console_format_str,
            datefmt=date_format_str,
            style="{",
            color_name=console_color_name,
            color_message=console_color_message,
            level_colors=console_level_colors,
        )
        console_handler.setFormatter(fmt=console_formatter)
        logger.addHandler(hdlr=console_handler)

    return logger


__all__ = ["get_logger"]
