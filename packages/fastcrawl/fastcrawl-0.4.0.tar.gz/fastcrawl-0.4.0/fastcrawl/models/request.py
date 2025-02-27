from typing import Optional, Union

from httpx import URL
from pydantic import BaseModel, ConfigDict

from fastcrawl.types import (
    Auth,
    Cookies,
    Files,
    FormData,
    Headers,
    JsonData,
    QueryParams,
    RequestCallback,
    RequestErrback,
)


class Request(BaseModel):
    """Request model.

    Attributes:
        method (str): HTTP method. Default is "GET".
        url (Union[URL, str]): URL to request.
        callback (RequestCallback): Callback to process the response.
        errback (Optional[RequestErrback]): Errback to process the error. Default is None.
        query_params (Optional[QueryParams]): Query parameters for the URL. Default is None.
        headers (Optional[Headers]): Headers for the request. Default is None.
        cookies (Optional[Cookies]): Cookies for the request. Default is None.
        form_data (Optional[FormData]): Form data for the request. Default is None.
        json_data (Optional[JsonData]): JSON data for the request. Default is None.
        files (Optional[Files]): Files for the request. Default is None.
        auth (Optional[Auth]): Authentication credentials. Default is None.
        timeout (Optional[float]): Timeout for the request in seconds. Default is None.
        follow_redirects (Optional[bool]): Whether to follow redirects. Default is None.

    """

    method: str = "GET"
    url: Union[URL, str]
    callback: RequestCallback
    errback: Optional[RequestErrback] = None
    query_params: Optional[QueryParams] = None
    headers: Optional[Headers] = None
    cookies: Optional[Cookies] = None
    form_data: Optional[FormData] = None
    json_data: Optional[JsonData] = None
    files: Optional[Files] = None
    auth: Optional[Auth] = None
    timeout: Optional[float] = None
    follow_redirects: Optional[bool] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}({self.method}, {self.url})>"
