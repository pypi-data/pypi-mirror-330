from zns_logging.ZnsLogger import ZnsLogger

logger = ZnsLogger(
    __name__,
    "DEBUG",
    file_path="test.log",
)

logger.debug("This is a debug message.")
logger.info("This is an info message.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
logger.critical("This is a critical message.")
