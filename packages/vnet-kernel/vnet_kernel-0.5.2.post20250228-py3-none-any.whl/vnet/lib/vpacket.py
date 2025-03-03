from __future__ import annotations

import random

from vnet.layers import IP, TCP, UDP, Ip4Header, TcpHeader, UdpHeader
from vnet.net_addr import Ip4Address


class VPacket:
    application_layer: bytes = b""
    transport_layer: TCP | UDP
    network_layer: IP
    rtt_range: tuple[int, int] = (0, 200)
    _rtt_ms: int = -1

    def __init__(
        self,
        application_layer: bytes | None = b"",
        transport_layer: TCP | UDP | None = None,
        network_layer: IP | None = None,
        rtt_range: tuple[int, int] | None = None,
    ):
        """
        Initialize a VPacket instance with optional application, transport, and network layers.

        Args:
                application_layer (bytes, optional): Data for the application layer. Defaults to b"".
                transport_layer (TCP | UDP, optional): Transport layer protocol. Defaults to None.
                network_layer (IP, optional): Network layer protocol. Defaults to None.
                rtt_range (tuple[int, int], optional): Range for RTT in ms. Defaults to (0, 200).
        """
        if application_layer is not None:
            self.application_layer = application_layer
        if transport_layer is not None:
            self.transport_layer = transport_layer
        if network_layer is not None:
            self.network_layer = network_layer
        if rtt_range is not None:
            self.rtt_range = rtt_range

    def __str__(self):
        """
        Return a string representation of the VPacket.

        Returns:
                str: Formatted string with source and destination addresses and ports, layers, and RTT.
        """
        return (
            f"{self.src_addr}:{self.src_port} >> {self.dst_addr}:{self.dst_port}\n"
            + f"ApplicationLayer = {self.application_layer},\n"
            + f"TransportLayer = {self.transport_layer}, \n"
            + f"NetworkLayer = {self.network_layer}, \n"
            + f"RTT = {self.rtt_ms}ms"
        )

    @property
    def transport_layer_header(self) -> TcpHeader | UdpHeader:
        return self.transport_layer.header

    @property
    def network_layer_header(self) -> Ip4Header:
        return self.network_layer.header

    @property
    def src_addr(self) -> Ip4Address:
        return self.network_layer.header.src

    @property
    def dst_addr(self) -> Ip4Address:
        return self.network_layer.header.dst

    # TODO 后期可以添加校验，tran_layer可能为空
    @property
    def src_port(self) -> int:
        return self.transport_layer.header.src_port

    @property
    def dst_port(self) -> int:
        return self.transport_layer.header.dst_port

    @property
    def rtt_ms(self) -> int:
        if self._rtt_ms == -1:
            self._rtt_ms = random.randint(*self.rtt_range)
        return self._rtt_ms

    def to_json(self, compact: bool = False) -> str:
        """
        Convert the VPacket instance to a JSON string.

        Args:
                compact (boolean, optional): If True, JSON will be compact without indentation. Defaults to False.

        Returns:
                str: JSON representation of the VPacket.
        """
        import json

        indent = 2
        if compact:
            indent = None
        # Convert the VPacket instance to a dictionary and then to JSON.
        return json.dumps(
            {
                "src_host": str(self.src_addr),
                "src_port": self.src_port,
                "dst_host": str(self.dst_addr),
                "dst_port": self.dst_port,
                "application_layer": self.application_layer.hex(),
                "transport_header": self.transport_layer.to_json if self.transport_layer else None,
                "network_header": self.network_layer.to_json if self.network_layer else None,
                "rtt_ms": self.rtt_ms,
            },
            indent=indent,
        )
