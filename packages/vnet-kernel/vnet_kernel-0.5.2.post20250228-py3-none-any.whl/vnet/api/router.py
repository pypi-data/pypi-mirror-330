from collections.abc import Callable


class RequestMapper:
    """用于路由方法，将请求路由到对应的处理函数，类似SpringBoot中的@RequestMapping"""

    routes: dict[str, dict[str, Callable]] = {
        "POST": {},
        "DELETE": {},
        "GET": {},
    }  # {"POST": {"/api/v1/netgroup": <function VNetController.create_network_group>, ...}, ...}

    @classmethod
    def route(cls, method: str, path: str):
        """装饰器工厂

        Args:
                method (str): HTTP 方法，例如 "POST"、"GET"、"DELETE"。
                path (str): 资源路径，例如 "/api/v1/netgroup"。

        Returns:
                Callable: 装饰过的函数。
        """

        def decorator(func: Callable):
            cls.routes.setdefault(method.upper(), {})[path] = func
            return func

        return decorator
