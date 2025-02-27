import logging

_APP_ROOT_LOGGER_NAME = "search-offline-evaluation"


def setup_logging(
    logger_name: str = "",
) -> logging.Logger:
    # Create a logger
    if logger_name == "":
        logger = logging.getLogger(_APP_ROOT_LOGGER_NAME)
    else:
        logger = logging.getLogger(f"{_APP_ROOT_LOGGER_NAME}.{logger_name}")
    return logger
