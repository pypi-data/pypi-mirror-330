from __future__ import annotations

import struct

from vnet.lib.constants import IP4_DEFAULT_TTL, IP4_PSEUDO_HEADER_STRUCT
from vnet.lib.inet_cksum import calc_inet_cksum
from vnet.lib.layer import Layer
from vnet.lib.proto_enum import IpProto
from vnet.net_addr import Ip4Address

from ..transport import TCP, UDP
from .ip4_header import (
    IP4__HEADER__LEN,
    Ip4Header,
    Ip4HeaderProperties,
)


class IP(Layer, Ip4HeaderProperties):
    """
    IPv4数据报

    该类表示一个IPv4数据报，包含头部和负载。
    提供了用于操作和访问数据报组件的方法和属性。
    暂时考虑不实现Option字段
    """

    header: Ip4Header
    payload: TCP | UDP
    payload_len: int
    _pshdr_sum: int = -1

    def __init__(
        self,
        *,
        src_addr: Ip4Address = Ip4Address(0),
        dst_addr: Ip4Address = Ip4Address(0),
        ttl: int = IP4_DEFAULT_TTL,
        dscp: int = 0,
        ecn: int = 0,
        id: int = 0,
        flag_df: bool = False,
        payload: TCP | UDP,
    ) -> None:
        """
        创建一个IPv4数据报实例

        Arguments:
                - src_addr (Ip4Address): 源IP地址，默认为0。
                - dst_addr (Ip4Address): 目标IP地址，默认为0。
                - ttl (int): 生存时间（Time To Live），默认为64。
                - dscp (int): 默认为0;
                - ecn (int):Explicit Congestion Notification
                - id (int): 数据报标识符，默认为0。
                - flag_df (bool): 不分片标志（Don't Fragment flag），默认为False。
                - payload (TCP | UDP): 负载数据，可以是TCP或UDP协议的数据。
        """

        self.payload = payload
        self.header = Ip4Header(
            dscp=dscp,
            inet_header_length=IP4__HEADER__LEN,
            ecn=ecn,
            total_length=IP4__HEADER__LEN + len(self.payload),
            identification=id,
            flag_df=flag_df,
            flag_mf=False,
            offset=0,
            ttl=ttl,
            proto=IpProto.from_protocol(payload),
            cksum=0,
            src=src_addr,
            dst=dst_addr,
        )
        self.payload_len = len(self.payload)

    def __len__(self) -> int:
        """
        返回Ip4数据报的总长度: header+payload
        """

        return len(self.header) + len(self.payload)

    def __str__(self) -> str:
        return (
            f"IPv4 {self.header.src} > {self.header.dst}, "
            f"proto {self.header.proto}, id {self.header.identification}"
            f"{', DF' if self.header.flag_df else ''}"
            f"{', MF' if self.header.flag_mf else ''}, "
            f"offset {self.header.offset}, ttl {self.header.ttl}, "
            f"len {self.header.total_length} "
            f"({len(self.header)}+{len(self.payload)})"
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(header={self.header!r}"

    def __bytes__(self) -> bytes:
        header = bytearray(bytes(self.header))
        header[10:12] = calc_inet_cksum(header).to_bytes(2)
        self.payload.pshdr_sum = self.pshdr_sum

        return bytes(header + bytes(self.payload))

    @property
    def pshdr_sum(self) -> int:
        """
        返回校验和。通过创建Ipv4伪首部，用于计算TCP、UDP和ICMPv4协议计算校验和。


        对于TCP和UDP的数据报，其首部也包含16位的校验和，由目的地接收端验证。校验算法与IPv4报文首部完全一致，但参与校验的数据不
        同。这时校验和不仅包含整个TCP/UDP数据报，还覆盖了一个伪首部。IPv4伪首部的定义如下

        ```shell
         0      7 8     15 16    23 24    31
        +--------+--------+--------+--------+
        |          source address           |
        +--------+--------+--------+--------+
        |        destination address        |
        +--------+--------+--------+--------+
        |  zero  |protocol| TCP/UDP length  |
        +--------+--------+--------+--------+
        ```
        """
        if self._pshdr_sum == -1:  # 为-1时，表示未计算过校验和
            pseudo_header = struct.pack(
                IP4_PSEUDO_HEADER_STRUCT,
                bytes(self.header.src),
                bytes(self.header.dst),
                0,
                int(self.header.proto),
                len(self.payload),
            )
            self._pshdr_sum = sum(struct.unpack("! 3L", pseudo_header))

        return self._pshdr_sum
