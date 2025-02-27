import logging
from abc import ABC, abstractmethod
from typing import Any, Optional

from fastcrawl.models.log_settings import LogSettings
from fastcrawl.utils.log import get_logger


class BasePipeline(ABC):
    """Base for all pipelines.

    Attributes:
        allowed_items (Optional[list[type]]): Allowed types of items to process.
            If provided, only items of these types will be processed and other items will be returned as is.
            If not provided, all items will be processed. Default is None.
        logger (logging.Logger): Logger for the crawler.

    """

    allowed_items: Optional[list[type]] = None
    logger: logging.Logger

    def __init__(self, log_settings: LogSettings) -> None:
        self.logger = get_logger(self.__class__.__name__, log_settings)

    @abstractmethod
    async def process_item(self, item: Any) -> Optional[Any]:
        """Processes an item returned by the crawler.

        Args:
            item (Any): Item to process.

        Returns:
            Any: Processed item.
            None: If the item should be dropped and not passed to the next pipelines.

        """

    async def on_start(self) -> None:
        """Called when the crawler starts."""

    async def on_finish(self) -> None:
        """Called when the crawler finishes."""

    async def process_allowed_item(self, item: Any) -> Optional[Any]:
        """Processes an item if it is allowed.

        Args:
            item (Any): Item to process.

        Returns:
            Any: Processed item.
            None: If the item should be dropped and not passed to the next pipelines.

        """
        if self.allowed_items is None or isinstance(item, tuple(self.allowed_items)):
            return await self.process_item(item)
        return item
