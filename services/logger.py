import sys
from loguru import logger
from config import LOG_FILE_PATH

def get_logger(name: str):
    """
    Returns a logger instance configured to write to console and a file.
    """
    # Ensure the logger is configured only once
    if len(logger._core.handlers) == 1: # The default handler
        logger.remove() # Remove default handler to prevent duplicate outputs
        # Console handler
        logger.add(
            sys.stderr,
            level="INFO",
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        )
        # File handler
        logger.add(
            LOG_FILE_PATH,
            rotation="10 MB",
            retention="7 days",
            level="DEBUG",
            enqueue=True,
            backtrace=True,
            diagnose=True,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
        )
    return logger.bind(name=name)

# Example of how to get a logger in another module:
# from services.logger import get_logger
# logger = get_logger(__name__)
