from __future__ import annotations

import struct
from abc import ABC
from dataclasses import dataclass
from typing import Any

from vnet.lib.constants import UDP__HEADER__LEN, UDP__HEADER__STRUCT


@dataclass(frozen=True, kw_only=True)
class UdpHeader:
    """
    The UDP packet header.
    """

    src_port: int
    dst_port: int
    udp_header_length: int
    cksum: int

    def __len__(self) -> int:
        return UDP__HEADER__LEN

    def __bytes__(self) -> bytes:
        return struct.pack(
            UDP__HEADER__STRUCT,
            self.src_port,
            self.dst_port,
            self.udp_header_length,
            0,
        )

    @staticmethod
    def from_bytes(_bytes: bytes, /) -> UdpHeader:
        src_port, des_port, header_len, cksum = struct.unpack(
            UDP__HEADER__STRUCT, _bytes[:UDP__HEADER__LEN]
        )

        return UdpHeader(
            src_port=src_port,
            dst_port=des_port,
            udp_header_length=header_len,
            cksum=cksum,
        )


class UdpHeaderProperties(ABC):
    header: UdpHeader

    @property
    def src_port(self) -> int:
        return self.header.src_port

    @property
    def dst_port(self) -> int:
        return self.header.dst_port

    @property
    def udp_header_length(self) -> int:
        return self.header.udp_header_length

    @property
    def cksum(self) -> int:
        return self.header.cksum

    @property
    def to_json(self) -> dict[str, Any]:
        return {
            "src_port": self.src_port,
            "dst_port": self.dst_port,
            "cksum": self.cksum,
            "udp_header_bytes": bytes(self.header).hex(),
        }
