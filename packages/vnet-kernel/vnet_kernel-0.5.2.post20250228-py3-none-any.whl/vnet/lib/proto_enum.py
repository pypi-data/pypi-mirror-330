from __future__ import annotations

from enum import Enum

from vnet.lib.layer import Layer


class IpProto(Enum):
    IP4 = 0
    ICMP4 = 1
    TCP = 6
    UDP = 17
    RAW = 255

    def __int__(self) -> int:
        return int(self.value)

    def __str__(self) -> str:
        """
        Get the value as a string.
        """

        match self:
            case IpProto.IP4:
                return "IPv4"
            case IpProto.ICMP4:
                return "ICMPv4"
            case IpProto.TCP:
                return "TCP"
            case IpProto.UDP:
                return "UDP"
            case _:
                raise ValueError(f"Unknown IP protocol {self.value}")

    @staticmethod
    def from_int(value: int) -> IpProto:
        """
        Get the IP protocol from an integer.
        """

        match value:
            case 0:
                return IpProto.IP4
            case 1:
                return IpProto.ICMP4
            case 6:
                return IpProto.TCP
            case 17:
                return IpProto.UDP
            case 255:
                return IpProto.RAW
            case _:
                raise ValueError(f"Unknown IP protocol {value}")

    @staticmethod
    def from_protocol(protocol: Layer) -> IpProto:
        """
        Get the IP protocol from a protocol.
        """
        from vnet.layers.transport.tcp import TCP
        from vnet.layers.transport.udp import UDP

        match protocol:
            case TCP():
                return IpProto.TCP
            case UDP():
                return IpProto.UDP
            case _:
                raise ValueError(f"Unknown protocol {protocol}")
