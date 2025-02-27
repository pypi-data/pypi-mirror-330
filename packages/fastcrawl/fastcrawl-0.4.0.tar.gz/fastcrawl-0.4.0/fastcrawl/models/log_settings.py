from pathlib import Path
from typing import Optional, Union

from pydantic import BaseModel


class LogSettings(BaseModel):
    """Log settings model.

    Attributes:
        configure_globally (bool): Whether to configure logging globally. Default is True.
        level (str): Log level. Default is "INFO".
        logger_name_suffix (Optional[str]): Suffix to add to logger name. Default is None.
        format (str): Log format. Default is "%(asctime)s [%(name)s] %(levelname)s: %(message)s".
        file (Optional[Union[Path, str]]): File to write logs to. Default is None.
        level_asyncio (str): Log level for asyncio library. Default is "WARNING".
        level_httpx (str): Log level for httpx library. Default is "WARNING".
        level_httpcore (str): Log level for httpcore library. Default is "WARNING".

    """

    configure_globally: bool = True
    level: str = "INFO"
    logger_name_suffix: Optional[str] = None
    format: str = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
    file: Optional[Union[Path, str]] = None
    level_asyncio: str = "WARNING"
    level_httpx: str = "WARNING"
    level_httpcore: str = "WARNING"
