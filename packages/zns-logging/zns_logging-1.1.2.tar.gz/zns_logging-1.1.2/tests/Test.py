from zns_logging import ZnsLogger
from zns_logging.utility.LogUtility import log_and_raise

logger = ZnsLogger(__name__, "DEBUG", file_path="logs/log.log")

logger.debug("This is a debug message.")
logger.info("This is an info message.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
logger.critical("This is a critical message.")

log_and_raise("Log and raise test.", ValueError, logger)