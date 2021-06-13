import logging
from ..config.paths import LOGS_PATH
from pathlib import Path
from pythonjsonlogger import jsonlogger


def get_logger() -> logging.getLogger:
    """Initializes a logger which is utilized by the click commands.

    :return: Returns a logger.
    :rtype: logging.getLogger
    """

    # Initialize loggers
    logger = logging.getLogger(__name__)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_format)

    # File handler
    try:
        file_handler = logging.FileHandler(str(LOGS_PATH / "absorb-logs.log"))
    except FileNotFoundError:
        Path(str(LOGS_PATH)).mkdir()
        Path(str(LOGS_PATH / "absorb-logs.log")).touch()
        file_handler = logging.FileHandler(str(LOGS_PATH / "absorb-logs.log"))

    file_handler.setLevel(logging.ERROR)

    JSON_formatter = jsonlogger.JsonFormatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(JSON_formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
