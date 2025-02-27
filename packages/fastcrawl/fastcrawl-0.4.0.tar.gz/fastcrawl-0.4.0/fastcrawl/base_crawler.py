import asyncio
import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, AsyncIterator, Optional

from httpx import AsyncClient, Limits

from fastcrawl.models import CrawlerSettings, CrawlerStats, Request, Response
from fastcrawl.utils.log import get_logger, setup_logging

if TYPE_CHECKING:
    from fastcrawl.base_pipeline import BasePipeline  # pragma: no cover


class BaseCrawler(ABC):
    """Base for all crawlers.

    Args:
        settings (Optional[CrawlerSettings]): Settings for the crawler.
            If not provided, the default settings will be used. Default is None.

    Attributes:
        logger (logging.Logger): Logger for the crawler.
        settings (CrawlerSettings): Settings for the crawler. Override it to set custom settings.
        stats (CrawlerStats): Statistics for the crawler.

    """

    logger: logging.Logger
    settings: CrawlerSettings = CrawlerSettings()
    stats: CrawlerStats

    _pipelines: list["BasePipeline"]
    _queue: asyncio.Queue
    _http_client: AsyncClient

    def __init__(self, settings: Optional[CrawlerSettings] = None) -> None:
        if settings:
            self.settings = settings

        setup_logging(self.settings.log)
        self.logger = get_logger(self.__class__.__name__, self.settings.log)
        self.stats = CrawlerStats()

        self._pipelines = [pipeline(self.settings.log) for pipeline in self.settings.pipelines]
        self._queue = asyncio.Queue()
        self._http_client = AsyncClient(**self._get_http_client_kwargs())

    def _get_http_client_kwargs(self) -> dict[str, Any]:
        kwargs = self.settings.http_client.model_dump()
        kwargs["params"] = kwargs.pop("query_params")
        kwargs["trust_env"] = False
        kwargs["limits"] = Limits(
            max_connections=kwargs.pop("max_connections"),
            max_keepalive_connections=kwargs.pop("max_keepalive_connections"),
            keepalive_expiry=kwargs.pop("keepalive_expiry"),
        )
        return kwargs

    async def on_start(self) -> None:
        """Called when the crawler starts."""

    async def on_finish(self) -> None:
        """Called when the crawler finishes."""

    @abstractmethod
    async def generate_requests(self) -> AsyncIterator[Request]:
        """Yields requests to be processed."""
        if False:  # pylint: disable=W0125  # pragma: no cover
            yield Request(url="https://example.com/", callback=lambda _: None)  # just a stub for mypy

    async def run(self) -> None:
        """Runs the crawler."""
        self.logger.info("Running crawler with settings: %s", self.settings.model_dump_json(indent=2))
        self.stats.start_crawling()
        await self.on_start()
        for pipeline in self._pipelines:
            await pipeline.on_start()

        async for request in self.generate_requests():
            await self._queue.put(request)

        workers = [asyncio.create_task(self._worker()) for _ in range(self.settings.workers)]
        await self._queue.join()
        for worker in workers:
            worker.cancel()

        await self._http_client.aclose()

        await self.on_finish()
        for pipeline in self._pipelines:
            await pipeline.on_finish()
        self.stats.finish_crawling()
        self.logger.info("Crawling finished with stats: %s", self.stats.model_dump_json(indent=2))

    async def _worker(self) -> None:
        while True:
            request = await self._queue.get()
            try:
                await self._process_request(request)
            except Exception as exc:  # pylint: disable=W0718
                self.logger.error("Error processing request %s: %s", request, exc)
            finally:
                self._queue.task_done()

    async def _process_request(self, request: Request) -> None:
        self.logger.debug("Processing request: %s", request)
        self.stats.add_request()

        httpx_response = await self._http_client.request(**self._get_request_kwargs(request))
        response = await Response.from_httpx_response(httpx_response, request)
        self.logger.debug("Got response: %s", response)
        self.stats.add_response(response.status_code)

        if httpx_response.is_success or response.status_code in self.settings.additional_success_status_codes:
            result = request.callback(response)
        elif request.errback:
            result = request.errback(response)
        else:
            self.logger.warning("Response not processed, cause no errback provided: %s", response)
            return

        if hasattr(result, "__aiter__"):
            async for item in result:
                if isinstance(item, Request):
                    await self._queue.put(item)
                elif item is not None:
                    for pipeline in self._pipelines:
                        item = await pipeline.process_allowed_item(item)
                        if item is None:
                            break
                    else:
                        self.stats.add_item()
        else:
            await result

    def _get_request_kwargs(self, request: Request) -> dict[str, Any]:
        kwargs = request.model_dump(exclude_none=True, exclude={"callback", "errback"})
        if "query_params" in kwargs:
            kwargs["params"] = kwargs.pop("query_params")
        if "form_data" in kwargs:
            kwargs["data"] = kwargs.pop("form_data")
        if "json_data" in kwargs:
            kwargs["json"] = kwargs.pop("json_data")
        return kwargs
