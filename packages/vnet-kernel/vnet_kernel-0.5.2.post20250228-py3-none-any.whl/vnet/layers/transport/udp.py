from __future__ import annotations


from vnet.lib.inet_cksum import calc_inet_cksum
from vnet.lib.layer import Layer

from .udp_header import (
    UDP__HEADER__LEN,
    UdpHeader,
    UdpHeaderProperties,
)


class UDP(Layer, UdpHeaderProperties):
    """
    Packet assembler interface for the UDP protocol.
    """

    header: UdpHeader
    payload: memoryview | bytes
    pshdr_sum: int = 0

    def __init__(
        self,
        *,
        udp_src_port: int = 0,
        udp_dst_port: int = 0,
        udp__payload: bytes | None = None,
    ) -> None:
        """
        Create packet assembler for the UDP protocol.
        """

        assert 0 <= udp_src_port <= 0xFFFF
        assert 0 <= udp_dst_port <= 0xFFFF

        self.payload = b"" if udp__payload is None else udp__payload
        self.header = UdpHeader(
            src_port=udp_src_port,
            dst_port=udp_dst_port,
            udp_header_length=UDP__HEADER__LEN + len(self.payload),
            cksum=0,
        )

    def __len__(self) -> int:
        """
        Get the UDP packet length.
        """

        return len(self.header) + len(self.payload)

    def __str__(self) -> str:
        """
        Get the UDP packet log string.
        """

        return (
            f"UDP {self.header.src_port} > {self.header.dst_port}, "
            f"len {self.header.udp_header_length} "
            f"({len(self.header)}+{self.header.udp_header_length - len(self.header)})"
        )

    def __repr__(self) -> str:
        """
        Get the UDP packet representation string.
        """

        return f"{self.__class__.__name__}(header={self.header!r}, " f"payload={self.payload!r})"

    def __bytes__(self) -> bytes:
        """
        Get the UDP packet as bytes.
        """

        _bytes = bytearray(bytes(self.header) + self.payload)
        _bytes[6:8] = calc_inet_cksum(_bytes, self.pshdr_sum).to_bytes(2)

        return bytes(_bytes)
