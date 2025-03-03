from __future__ import annotations

import struct
from abc import ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

from vnet.lib.constants import TCP__HEADER__LEN, TCP__HEADER__STRUCT


@dataclass(frozen=True, kw_only=True)
class TcpHeader:
    src_port: int
    dst_port: int
    seq: int
    ack: int
    hlen: int
    flag_ns: bool
    flag_cwr: bool
    flag_ece: bool
    flag_urg: bool
    flag_ack: bool
    flag_psh: bool
    flag_rst: bool
    flag_syn: bool
    flag_fin: bool
    win: int
    cksum: int
    urg: int

    @staticmethod
    def from_bytes(_bytes: bytes, /) -> TcpHeader:
        src_port, dst_port, seq, ack, hlen__flags, win, cksum, urg = struct.unpack(
            TCP__HEADER__STRUCT, _bytes[:TCP__HEADER__LEN]
        )

        return TcpHeader(
            src_port=src_port,
            dst_port=dst_port,
            seq=seq,
            ack=ack,
            hlen=(hlen__flags & 0b11110000_00000000) >> 10,
            flag_ns=bool(hlen__flags & 0b00000001_00000000),
            flag_cwr=bool(hlen__flags & 0b00000000_10000000),
            flag_ece=bool(hlen__flags & 0b00000000_01000000),
            flag_urg=bool(hlen__flags & 0b00000000_00100000),
            flag_ack=bool(hlen__flags & 0b00000000_00010000),
            flag_psh=bool(hlen__flags & 0b00000000_00001000),
            flag_rst=bool(hlen__flags & 0b00000000_00000100),
            flag_syn=bool(hlen__flags & 0b00000000_00000010),
            flag_fin=bool(hlen__flags & 0b00000000_00000001),
            win=win,
            cksum=cksum,
            urg=urg,
        )

    def __len__(self) -> int:
        return TCP__HEADER__LEN

    def __bytes__(self) -> bytes:
        return struct.pack(
            TCP__HEADER__STRUCT,
            self.src_port,
            self.dst_port,
            self.seq,
            self.ack,
            self.hlen << 10
            | self.flag_ns << 8
            | self.flag_cwr << 7
            | self.flag_ece << 6
            | self.flag_urg << 5
            | self.flag_ack << 4
            | self.flag_psh << 3
            | self.flag_rst << 2
            | self.flag_syn << 1
            | self.flag_fin,
            self.win,
            0,
            self.urg,
        )


class TcpHeaderProperties(ABC):
    header: TcpHeader

    @property
    def src_port(self) -> int:
        return self.header.src_port

    @property
    def dst_port(self) -> int:
        return self.header.dst_port

    @property
    def seq(self) -> int:
        return self.header.seq

    @property
    def ack(self) -> int:
        return self.header.ack

    @property
    def hlen(self) -> int:
        return self.header.hlen

    @property
    def flag_ns(self) -> bool:
        return self.header.flag_ns

    @property
    def flag_cwr(self) -> bool:
        return self.header.flag_cwr

    @property
    def flag_ece(self) -> bool:
        return self.header.flag_ece

    @property
    def flag_urg(self) -> bool:
        return self.header.flag_urg

    @property
    def flag_ack(self) -> bool:
        return self.header.flag_ack

    @property
    def flag_psh(self) -> bool:
        return self.header.flag_psh

    @property
    def flag_rst(self) -> bool:
        return self.header.flag_rst

    @property
    def flag_syn(self) -> bool:
        return self.header.flag_syn

    @property
    def flag_fin(self) -> bool:
        return self.header.flag_fin

    @property
    def win(self) -> int:
        return self.header.win

    @property
    def cksum(self) -> int:
        return self.header.cksum

    @property
    def urg(self) -> int:
        return self.header.urg

    @property
    def to_json(self) -> dict[str, Any]:
        return {
            "src_port": self.src_port,
            "dst_port": self.dst_port,
            "seq": self.seq,
            "ack": self.ack,
            "hlen": self.hlen,
            "flag_ns": self.flag_ns,
            "flag_cwr": self.flag_cwr,
            "flag_ece": self.flag_ece,
            "flag_urg": self.flag_urg,
            "flag_ack": self.flag_ack,
            "flag_psh": self.flag_psh,
            "flag_rst": self.flag_rst,
            "flag_syn": self.flag_syn,
            "flag_fin": self.flag_fin,
            "win": self.win,
            "cksum": self.cksum,
            "urg": self.urg,
            "tcp_header_bytes": bytes(self.header).hex(),
        }
