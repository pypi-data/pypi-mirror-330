from .http_header import HttpHeader
from vnet.lib.layer import Layer


class HTTP(Layer):
    header: HttpHeader
    body: bytes

    def __init__(
        self,
        *,
        method: str = "GET",
        url: str = "/",
        version: str = "HTTP/1.1",
        headers: dict[str, str] | None = None,
        body: bytes = bytes(),
    ) -> None:
        self.body = body
        self.header = HttpHeader(method=method, url=url, version=version, headers=headers)

        # 自动添加Content-Length头部，除非已指定
        if "Content-Length" not in self.header.headers:
            self.header.headers["Content-Length"] = str(len(self.body))

    def __len__(self) -> int:
        """
        获取HTTP报文的长度 (头部 + 负载)
        """
        return len(self.header) + len(self.body)

    def __str__(self) -> str:
        try:
            # 将HTTP头和负载内容拼接为字符串
            return str(self.header) + self.body.decode("utf-8", errors="ignore")
        except AttributeError as e:
            return f"HTTP_Assembler_Error: {e}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(header={self.header!r}, body={self.body!r})"

    def __bytes__(self) -> bytes:
        """
        返回HTTP报文的字节表示形式
        """
        return bytes(self.header) + self.body
