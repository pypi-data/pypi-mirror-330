import inspect
import logging
from typing import Type


def log_and_raise(
    message: str,
    exception_type: Type[Exception],
    logger: logging.Logger,
    error: Exception = None,
) -> None:
    """
    Logs an error message and raises an exception.

    :param name: The name of the module or class that called this function.
    :param message: The error message.
    :param exception_type: The exception type to raise.
    :param logger: Optional logger to log the error message. Defaults to a module-level logger.
    :param error: Optional exception that caused this error (for exception chaining).
    :raises exception_type: Always raises the specified exception with the given message.
    """

    if not issubclass(exception_type, Exception):
        raise TypeError("exception_type must be a subclass of Exception")

    filename = inspect.stack()[1].filename
    name = inspect.getmodulename(filename)

    log = f"{message} - Module: [{name}]"
    logger.error(log)
    raise exception_type(log) from error


__all__ = ["log_and_raise"]
