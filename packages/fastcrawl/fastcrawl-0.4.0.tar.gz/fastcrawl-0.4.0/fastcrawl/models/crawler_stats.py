from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CrawlerStats(BaseModel):
    """Crawler statistics model.

    Note:
        To update statistics while crawling, use corresponding methods.

    Attributes:
        started_at (Optional[datetime]): The time when the crawling started. Default is None.
        finished_at (Optional[datetime]): The time when the crawling finished. Default is None.
        requests (Optional[int]): The number of requests made during the crawling. Default is None.
        responses_by_codes (Optional[dict[int, int]]): The number of responses by status code. Default is None.
        items (Optional[int]): The number of items crawled. Default is None.

    """

    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    requests: Optional[int] = None
    responses_by_codes: Optional[dict[int, int]] = None
    items: Optional[int] = None

    def start_crawling(self) -> None:
        """Sets the time when the crawling started."""
        self.started_at = datetime.now()

    def finish_crawling(self) -> None:
        """Sets the time when the crawling finished."""
        self.finished_at = datetime.now()

    def add_request(self) -> None:
        """Increases the number of requests made during the crawling."""
        if self.requests:
            self.requests += 1
        else:
            self.requests = 1

    def add_response(self, status_code: int) -> None:
        """Increases the number of responses by status code."""
        if self.responses_by_codes is None:
            self.responses_by_codes = {}

        if status_code in self.responses_by_codes:
            self.responses_by_codes[status_code] += 1
        else:
            self.responses_by_codes[status_code] = 1

    def add_item(self) -> None:
        """Increases the number of items crawled."""
        if self.items:
            self.items += 1
        else:
            self.items = 1
