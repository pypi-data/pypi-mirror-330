import logging
from typing import Literal

from colorama import init, Fore, Style

init(autoreset=True)

class LogConsoleFormatter(logging.Formatter):
    DEFAULT_LEVEL_COLORS = {
        "DEBUG": Fore.BLUE,
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.MAGENTA,
    }

    def __init__(
        self,
        fmt: str = None,
        datefmt: str = None,
        style: Literal["%", "{", "$"] = "{",
        validate: bool = True,
        *,
        color_name: str = Fore.CYAN,
        color_message: str = Fore.RESET,
        level_colors: dict[str, str] = None,
        **kwargs,
    ):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style, validate=validate, **kwargs)
        self.color_name = color_name
        self.color_message = color_message
        self.level_colors = level_colors or self.DEFAULT_LEVEL_COLORS

    def format(self, record: logging.LogRecord) -> str:
        record.levelname = f"{self.level_colors.get(record.levelname, Fore.RESET)}{record.levelname:8}{Style.RESET_ALL}"
        record.name = f"{self.color_name}{record.name}{Style.RESET_ALL}"
        record.msg = f"{self.color_message}{record.msg}{Style.RESET_ALL}"

        return super().format(record)
