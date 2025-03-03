from __future__ import annotations

import struct
from abc import ABC
from dataclasses import dataclass, field, replace
from typing import TYPE_CHECKING

from vnet.lib.constants import IP4__HEADER__LEN, IP4__HEADER__STRUCT, IP4_DEFAULT_TTL
from vnet.lib.proto_enum import IpProto
from vnet.net_addr import Ip4Address

if TYPE_CHECKING:
    from typing import Any


@dataclass(frozen=True)
class Ip4Header:
    """
    表示 IPv4 数据报的首部
    """

    version: int = field(repr=False, init=False, default=4)
    inet_header_length: int = field(default=IP4__HEADER__LEN)  # 首部长度, 默认20字节
    dscp: int = field(default=0)  # 区分服务字段
    ecn: int = field(
        default=0
    )  # 显式拥塞通知，相比于TCP的拥塞控制，ECN是一种更加轻量级的拥塞控制机制
    total_length: int = field(default=IP4__HEADER__LEN)  # 首部+数据长度
    identification: int = field(default=0)  # 标识符
    flag_df: bool = field(default=False)
    flag_mf: bool = field(default=False)
    offset: int = field(default=0)
    ttl: int = field(default=IP4_DEFAULT_TTL)
    proto: IpProto = field(default=IpProto.IP4)  # 默认0
    cksum: int = field(default=0)  # 首部校验和，初始化为0
    src: Ip4Address = field(default=Ip4Address(0))
    dst: Ip4Address = field(default=Ip4Address(0))

    def __len__(self) -> int:
        """
        返回ip4 header长度
        """
        return IP4__HEADER__LEN

    def __bytes__(self) -> bytes:
        """
        返回该报文头对应的字节流
        """

        return struct.pack(
            IP4__HEADER__STRUCT,
            self.version << 4 | self.inet_header_length >> 2,
            self.dscp << 2 | self.ecn,
            self.total_length,
            self.identification,
            self.flag_df << 14 | self.flag_mf << 13 | self.offset >> 3,
            self.ttl,
            int(self.proto),
            0,
            int(self.src),
            int(self.dst),
        )

    @staticmethod
    def from_bytes(_bytes: bytes) -> Ip4Header:
        (
            ver_hlen,
            dscp__ecn,
            total_length,
            identification,
            flag__offset,
            ttl,
            proto,
            cksum,
            src,
            dst,
        ) = struct.unpack(IP4__HEADER__STRUCT, _bytes[:IP4__HEADER__LEN])

        return Ip4Header(
            inet_header_length=(ver_hlen & 0b00001111) << 2,
            dscp=dscp__ecn >> 2,
            ecn=dscp__ecn & 0b00000011,
            total_length=total_length,
            identification=identification,
            flag_df=bool(flag__offset >> 8 & 0b01000000),
            flag_mf=bool(flag__offset >> 8 & 0b00100000),
            offset=(flag__offset & 0b0001111111111111) << 3,
            ttl=ttl,
            proto=IpProto.from_int(proto),
            cksum=cksum,
            src=Ip4Address(src),
            dst=Ip4Address(dst),
        )

    def set_src_addr(self, src: str | Ip4Address) -> "Ip4Header":
        """Set source IP address and return new header instance."""
        src_addr = Ip4Address(src) if isinstance(src, str) else src
        return replace(self, src=src_addr)

    def set_dest_addr(self, dst: str | Ip4Address) -> "Ip4Header":
        """Set destination IP address and return new header instance."""
        dst_addr = Ip4Address(dst) if isinstance(dst, str) else dst
        return replace(self, dst=dst_addr)


class Ip4HeaderProperties(ABC):
    header: Ip4Header

    @property
    def version(self) -> int:
        return self.header.version

    @property
    def inet_header_length(self) -> int:
        return self.header.inet_header_length

    @property
    def dscp(self) -> int:
        return self.header.dscp

    @property
    def ecn(self) -> int:
        return self.header.ecn

    @property
    def total_length(self) -> int:
        return self.header.total_length

    @property
    def identification(self) -> int:
        return self.header.identification

    @property
    def flag_df(self) -> bool:
        return self.header.flag_df

    @property
    def flag_mf(self) -> bool:
        return self.header.flag_mf

    @property
    def offset(self) -> int:
        return self.header.offset

    @property
    def ttl(self) -> int:
        return self.header.ttl

    @property
    def proto(self) -> IpProto:
        return self.header.proto

    @property
    def cksum(self) -> int:
        return self.header.cksum

    @property
    def src(self) -> Ip4Address:
        return self.header.src

    @property
    def dst(self) -> Ip4Address:
        return self.header.dst

    @property
    def to_json(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "inet_header_length": self.inet_header_length,
            "dscp": self.dscp,
            "ecn": self.ecn,
            "total_length": self.total_length,
            "identif": self.identification,
            "flag_df": self.flag_df,
            "flag_mf": self.flag_mf,
            "offset": self.offset,
            "ttl": self.ttl,
            "proto": str(self.proto),
            "cksum": self.cksum,
            "src": str(self.src),
            "dst": str(self.dst),
            "ip4_header_bytes": bytes(self.header).hex(),
        }
