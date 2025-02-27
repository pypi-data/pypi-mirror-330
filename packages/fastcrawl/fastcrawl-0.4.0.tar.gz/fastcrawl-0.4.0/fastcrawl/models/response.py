import json
from typing import Any, Optional

from httpx import URL
from httpx import Response as HttpxResponse
from httpx import ResponseNotRead
from parsel import Selector
from pydantic import BaseModel, ConfigDict, PrivateAttr

from fastcrawl.models.request import Request


class Response(BaseModel):
    """Response model.

    Attributes:
        url (URL): URL of the response.
        status_code (int): Status code of the response.
        content (bytes): Content of the response.
        text (str): Text of the response.
        headers (Optional[dict[str, str]]): Headers of the response. Default is None.
        cookies (Optional[dict[str, str]]): Cookies of the response. Default is None.
        request (Request): Request used to fetch the response.

    """

    url: URL
    status_code: int
    content: bytes
    text: str
    headers: Optional[dict[str, str]] = None
    cookies: Optional[dict[str, str]] = None
    request: Request
    _cached_selector: Optional[Selector] = PrivateAttr(default=None)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    async def from_httpx_response(cls, httpx_response: HttpxResponse, request: Request) -> "Response":
        """Returns new instance from an httpx response.

        Args:
            httpx_response (HttpxResponse): Response from httpx.
            request (Request): Request used to fetch the response.

        """
        try:
            content = httpx_response.content
        except ResponseNotRead:
            content = await httpx_response.aread()

        return cls(
            url=httpx_response.url,
            status_code=httpx_response.status_code,
            content=content,
            text=httpx_response.text,
            headers=dict(httpx_response.headers),
            cookies=dict(httpx_response.cookies),
            request=request,
        )

    def get_json_data(self) -> Any:
        """Returns JSON data from the response."""
        return json.loads(self.text)

    @property
    def selector(self) -> Selector:
        """Selector for xpath and css queries."""
        if self._cached_selector is None:
            self._cached_selector = Selector(text=self.text)
        return self._cached_selector

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}({self.status_code}, {self.url})>"
