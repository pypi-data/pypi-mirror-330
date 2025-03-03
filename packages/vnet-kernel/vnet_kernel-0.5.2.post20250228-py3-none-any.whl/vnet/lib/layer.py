from abc import ABC, abstractmethod


class Layer(ABC):
    """
    所有协议类的abstract类。

    需要实现以下方法：
    - __init__
    - __len__
    - __str__
    - __repr__
    - __bytes__
    - __eq__
    - __hash__
    """

    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def __bytes__(self) -> bytes:
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Layer) and repr(self) == repr(other)

    def __hash__(self) -> int:
        return hash(repr(self))
