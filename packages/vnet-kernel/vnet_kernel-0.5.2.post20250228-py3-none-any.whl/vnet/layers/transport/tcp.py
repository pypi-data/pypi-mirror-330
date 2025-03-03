from __future__ import annotations


from vnet.lib.constants import TCP__HEADER__LEN
from vnet.lib.inet_cksum import calc_inet_cksum
from vnet.lib.layer import Layer

from .tcp_header import (
    TcpHeader,
    TcpHeaderProperties,
)


class TCP(Layer, TcpHeaderProperties):
    header: TcpHeader
    payload: memoryview | bytes
    pshdr_sum: int = 0

    def __init__(
        self,
        *,
        src_port: int = 0,
        dst_port: int = 0,
        seq: int = 0,
        ack: int = 0,
        flag_ns: bool = False,
        flag_cwr: bool = False,
        flag_ece: bool = False,
        flag_urg: bool = False,
        flag_ack: bool = False,
        flag_psh: bool = False,
        flag_rst: bool = False,
        flag_syn: bool = False,
        flag_fin: bool = False,
        win: int = 0,
        urg: int = 0,
        payload: bytes = bytes(),
    ) -> None:
        self.payload = payload

        self.header = TcpHeader(
            src_port=src_port,
            dst_port=dst_port,
            seq=seq,
            ack=ack,
            hlen=TCP__HEADER__LEN,
            flag_ns=flag_ns,
            flag_cwr=flag_cwr,
            flag_ece=flag_ece,
            flag_urg=flag_urg,
            flag_ack=flag_ack,
            flag_psh=flag_psh,
            flag_rst=flag_rst,
            flag_syn=flag_syn,
            flag_fin=flag_fin,
            win=win,
            cksum=0,
            urg=urg,
        )

    def __len__(self) -> int:
        """
        Get the TCP packet length.(header+payload)
        """
        return len(self.header) + len(self.payload)

    def __str__(self) -> str:
        try:
            flags = [
                ("N", self.header.flag_ns),
                ("C", self.header.flag_cwr),
                ("E", self.header.flag_ece),
                ("U", self.header.flag_urg),
                ("A", self.header.flag_ack),
                ("P", self.header.flag_psh),
                ("R", self.header.flag_rst),
                ("S", self.header.flag_syn),
                ("F", self.header.flag_fin),
            ]
            flag_str = "".join(flag for flag, is_set in flags if is_set)
            flag_separator = ", " if flag_str else ""

            seq_ack_win = f"seq {self.header.seq}, ack {self.header.ack}, win {self.header.win}"
            urg = f"urg {self.header.urg}, " if self.header.flag_urg else ""
            length = f"len {len(self.header) + len(self.payload)} ({len(self.header)}+{len(self.payload)})"
        except AttributeError as e:
            return f"TCP_Assembler_Error: {e}"

        return (
            f"TCP {self.header.src_port} > {self.header.dst_port}, "
            f"{flag_str}{flag_separator}"
            f"{seq_ack_win}, "
            f"{urg}"
            f"{length}"
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(header={self.header!r}, " f"payload={self.payload!r})"

    def __bytes__(self) -> bytes:
        _bytes = bytearray(bytes(self.header) + self.payload)
        _bytes[16:18] = calc_inet_cksum(_bytes, self.pshdr_sum).to_bytes(2)

        return bytes(_bytes)
