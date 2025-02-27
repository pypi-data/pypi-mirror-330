from typing import Optional, Union

from httpx import URL
from pydantic import BaseModel, ConfigDict

from fastcrawl.types import Auth, Cookies, Headers, QueryParams


class HttpClientSettings(BaseModel):
    """HTTP client settings model.

    Attributes:
        base_url (Union[URL, str]): Base URL for the HTTP client. Default is "".
        auth (Optional[Auth]): Authentication for the HTTP client. Default is None.
        query_params (Optional[QueryParams]): Query parameters for the HTTP client. Default is None.
        headers (Optional[Headers]): Headers for the HTTP client. Default is None.
        cookies (Optional[Cookies]): Cookies for the HTTP client. Default is None.
        verify (bool): Whether to verify SSL certificates. Default is True.
        http1 (bool): Whether to use HTTP/1.1. Default is True.
        http2 (bool): Whether to use HTTP/2. Default is False.
        proxy (Optional[Union[URL, str]]): Proxy for the HTTP client. Default is None.
        timeout (float): Timeout for the HTTP client. Default is 5.0.
        max_connections (Optional[int]): Specifies the maximum number of concurrent connections allowed. Default is 100.
        max_keepalive_connections (Optional[int]): The maximum number of keep-alive connections the pool can maintain.
            Must not exceed `max_connections`. Default is 20.
        keepalive_expiry (Optional[float]): The maximum duration in seconds that a keep-alive
            connection can remain idle. Default is 5.0.
        follow_redirects (bool): Whether to follow redirects. Default is False.
        max_redirects (int): Maximum number of redirects to follow. Default is 20.
        default_encoding (str): Default encoding for the HTTP client. Default is "utf-8".

    """

    base_url: Union[URL, str] = ""
    auth: Optional[Auth] = None
    query_params: Optional[QueryParams] = None
    headers: Optional[Headers] = None
    cookies: Optional[Cookies] = None
    verify: bool = True
    http1: bool = True
    http2: bool = False
    proxy: Optional[Union[URL, str]] = None
    timeout: float = 5.0
    max_connections: Optional[int] = 100
    max_keepalive_connections: Optional[int] = 20
    keepalive_expiry: Optional[float] = 5.0
    follow_redirects: bool = False
    max_redirects: int = 20
    default_encoding: str = "utf-8"

    model_config = ConfigDict(arbitrary_types_allowed=True)
