import logging
import os
from logging.handlers import RotatingFileHandler

from colorama import Fore

from zns_logging.utility.LogConsoleFormatter import LogConsoleFormatter

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


def _check_level(level: int | str) -> int:
    if isinstance(level, str):
        level = logging.getLevelName(level.upper())
    elif isinstance(level, int):
        pass
    else:
        raise TypeError(f"Expected str or int, got {type(level).__name__}")

    if level not in _ALLOWED_LEVELS:
        raise ValueError(f"Expected one of {_ALLOWED_LEVELS}, got {level}")

    return level


def _create_file_handler(
    file_path: str,
    file_mode: str,
    file_max_bytes: int,
    file_backup_count: int,
    file_encoding: str,
    file_format_str: str,
    date_format_str: str,
) -> RotatingFileHandler:
    directory = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok=True)
    file_handler = RotatingFileHandler(
        filename=file_path,
        mode=file_mode,
        maxBytes=file_max_bytes,
        backupCount=file_backup_count,
        encoding=file_encoding,
    )
    file_formatter = logging.Formatter(file_format_str, datefmt=date_format_str)
    file_handler.setFormatter(file_formatter)

    return file_handler


def _create_console_handler(
    console_format_str: str,
    console_color_name: str,
    console_color_message: str,
    console_level_colors: dict[str, str],
) -> logging.StreamHandler:
    console_handler = logging.StreamHandler()
    console_formatter = LogConsoleFormatter(
        console_format_str,
        datefmt=_DATE_FORMAT_STR,
        color_name=console_color_name,
        color_message=console_color_message,
        level_colors=console_level_colors,
    )
    console_handler.setFormatter(console_formatter)

    return console_handler


class ZnsLogger(logging.Logger):
    def __init__(
        self,
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
    ):
        _check_level(level)

        super().__init__(name, level)

        if enable_file_logging and file_path:
            file_handler = _create_file_handler(
                file_path,
                file_mode,
                file_max_bytes,
                file_backup_count,
                file_encoding,
                file_format_str,
                date_format_str,
            )
            self.addHandler(file_handler)

        if enable_console_logging:
            console_handler = _create_console_handler(
                console_format_str,
                console_color_name,
                console_color_message,
                console_level_colors,
            )
            self.addHandler(console_handler)

        self.propagate = False


__all__ = ["ZnsLogger"]
