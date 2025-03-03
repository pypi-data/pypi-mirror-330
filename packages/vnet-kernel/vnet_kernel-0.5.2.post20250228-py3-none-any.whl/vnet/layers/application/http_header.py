from __future__ import annotations

from abc import ABC
from typing import Any


class HttpHeader:
    """
    用于HTTP头的简单结构，支持设置请求方法、URL、协议版本和常见的HTTP头字段。
    """

    def __init__(
        self,
        method: str = "GET",
        url: str = "/",
        version: str = "HTTP/1.1",
        headers: dict[str, str] | None = None,
    ) -> None:
        self.method = method
        self.url = url
        self.version = version
        self.headers = headers or {}

    def __str__(self) -> str:
        # 格式化HTTP请求头
        header_str = f"{self.method} {self.url} {self.version}\r\n"
        for key, value in self.headers.items():
            header_str += f"{key}: {value}\r\n"
        return header_str + "\r\n"

    def __bytes__(self) -> bytes:
        return str(self).encode("utf-8")

    def __len__(self) -> int:
        return len(bytes(self))


class HttpHeaderProperties(ABC):
    http_header: HttpHeader

    @property
    def method(self) -> str:
        return self.http_header.method

    @property
    def url(self) -> str:
        return self.http_header.url

    @property
    def version(self) -> str:
        return self.http_header.version

    @property
    def headers(self) -> dict[str, str]:
        return self.http_header.headers

    @property
    def to_json(self) -> dict[str, Any]:
        return {
            "method": self.method,
            "url": self.url,
            "version": self.version,
            "headers": self.headers,
        }
