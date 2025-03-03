# validation.py
from ipaddress import IPv4Address, IPv4Network
import logging
from collections.abc import Callable
from functools import wraps
from typing import Any

from .response_vo import ResponseVO

logger = logging.getLogger(__name__)


def validate_inet_addr(*param_names: str, param_type: str = "IPv4Address"):
    """Decorator that validates IPv4 addresses/network in parameters."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(self, *args, **kwargs) -> Any:
            # Combine args and kwargs into a single dict
            bound_args = dict(zip(func.__code__.co_varnames[1:], args))
            bound_args.update(kwargs)

            # Validate each specified parameter
            for param_name in param_names:
                if param_name in bound_args:
                    value = bound_args[param_name]
                    try:
                        if param_type == "IPv4Address":
                            IPv4Address(value)
                        elif param_type == "IPv4Network":
                            IPv4Network(value)
                        else:
                            raise ValueError(f"Unsupported param_type: {param_type}")
                    except ValueError:
                        return ResponseVO("[ERROR]", f"请检查地址格式: {value}")

            return func(self, *args, **kwargs)

        return wrapper

    return decorator
