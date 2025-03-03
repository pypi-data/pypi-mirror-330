import logging
from collections.abc import Callable
from enum import Enum
from functools import wraps
from typing import Any, TypeVar, cast


class Status(Enum):
    """
    - SUCCESS: 成功
    - NGRP_ALREADY_EXISTS: 要添加的Net Group已经存在
    - NGRP_NOT_FOUNT: 未找到相应的Net Group
    - CONN_NOT_FOUND: 未找到相应的连接
    - NOT_MATCH: Host 和 Network 不匹配
    - INVALID_ADDR_FORMAT: Ip地址格式错误
    """

    SUCCESS = ("Success", logging.INFO)
    NGRP_ALREADY_EXISTS = ("Net Group Already Exists", logging.INFO)
    NGRP_NOT_FOUND = ("Net Group Not Found", logging.WARNING)
    CONN_ALREADY_EXISTS = ("Connection Already Exists", logging.INFO)
    CONN_NOT_FOUND = ("Connection Not Found", logging.WARNING)
    HOST_ALREADY_EXISTS = ("Host Already Exists", logging.INFO)
    HOST_NOT_FOUND = ("Host Not Found", logging.WARNING)
    NOT_MATCH = ("Host and Network not match", logging.WARNING)
    ADD_FAILED = ("Add Failed", logging.ERROR)
    HOST_NOT_CONNECTED = ("Hosts Not Connected", logging.ERROR)
    INVALID_ADDR_FORMAT = ("Invalid Address Format", logging.ERROR)
    INVALID_VPACKET = ("Invalid VPacket", logging.ERROR)


# Create a generic callable return type for better type hinting
R = TypeVar("R")


def service_logger(func: Callable[..., R]) -> Callable[..., R]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> R:
        # Log the function name and input arguments
        logging.info("[Service] 调用 %s, 参数为: args=%s, kwargs=%s", func.__name__, args, kwargs)

        try:
            result = func(*args, **kwargs)
            logging.info("[Service] 函数 %s 执行完毕，返回值: %s", func.__name__, result)
        except Exception as e:
            logging.error(f"Exception in {func.__name__}: {e}", exc_info=True)
            raise

        return result

    return cast(Callable[..., R], wrapper)


def controller_logger(func):
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        logging.info(
            "[Controller] 调用 %s, 参数为: args=%s, kwargs=%s", func.__name__, args, kwargs
        )
        try:
            result = func(*args, **kwargs)
            logging.info("[Controller] 函数 %s 执行完毕，返回值: %s", func.__name__, result)
        except Exception as e:
            logging.info("[Controller] 函数 %s 执行时发生异常: %s", func.__name__, e)
            raise
        return result

    return wrapper
