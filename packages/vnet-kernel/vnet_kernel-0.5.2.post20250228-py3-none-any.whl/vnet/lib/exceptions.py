from typing import Any


class NetAddrError(Exception):
    """
    所有NetAddr异常的基础类。
    """


class Ip4AddressFormatError(NetAddrError):
    """
    当IPv4地址格式无效时引发的异常。
    """

    def __init__(self, message: Any, /):
        super().__init__(f"IPv4地址格式无效: {message!r}")


class Ip4NetworkFormatError(NetAddrError):
    """
    当IPv4网络格式无效时引发的异常。
    """

    def __init__(self, message: Any, /):
        super().__init__(f"IPv4网络格式无效: {message!r}")


class Ip4HostFormatError(NetAddrError):
    """
    当IPv4主机格式无效时引发的异常。
    """

    def __init__(self, message: Any, /):
        super().__init__(f"IPv4主机格式无效: {message!r}")
