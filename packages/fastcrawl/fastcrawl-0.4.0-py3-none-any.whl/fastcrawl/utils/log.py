import logging
from logging import FileHandler, Formatter, Logger

from fastcrawl.models.log_settings import LogSettings


def setup_logging(settings: LogSettings) -> None:
    """Sets up logging based on the provided settings.

    Args:
        settings (LogSettings): Settings for the logging.

    """
    if settings.configure_globally:
        logging.basicConfig(level=settings.level, format=settings.format)

    logging.getLogger("asyncio").setLevel(settings.level_asyncio)
    logging.getLogger("httpx").setLevel(settings.level_httpx)
    logging.getLogger("httpcore").setLevel(settings.level_httpcore)


def get_logger(name: str, settings: LogSettings) -> Logger:
    """Returns a logger with the provided name and settings.

    Args:
        name (str): Name of the logger.
        settings (LogSettings): Settings for the logging.

    """
    if settings.logger_name_suffix:
        name += f"_{settings.logger_name_suffix}"

    logger = logging.getLogger(name)
    logger.setLevel(settings.level)

    if settings.file:
        logger.addHandler(FileHandler(settings.file))

    formatter = Formatter(settings.format)
    for handler in logger.handlers:
        handler.setFormatter(formatter)

    return logger
