from dataclasses import dataclass
from ipaddress import IPv4Address, IPv4Interface, IPv4Network


@dataclass
class Ip4Host:
    """
    IPv4 host support class.
    """

    ip_address: IPv4Address
    ip_network: IPv4Network
    ip_interface: IPv4Interface

    def __repr__(self) -> str:
        return f"Ip4Host('{self.ip_interface}')"


class Ip4HostFactory:
    @staticmethod
    def from_interface(ip_intf: str | IPv4Interface) -> Ip4Host:
        if isinstance(ip_intf, str):
            ip_intf = IPv4Interface(ip_intf)
        ip_address = ip_intf.ip
        ip_network = ip_intf.network
        return Ip4Host(ip_address, ip_network, ip_intf)

    @staticmethod
    def from_address_and_network(
        ip_addr: str | IPv4Address, network_addr: str | IPv4Network
    ) -> Ip4Host:
        """
        Args:
                ip_addr (str | IPv4Address): 192.168.1.1 e.g.
                net: (str | IPv4Network): 192.168.1.0/32 e.g.
        """
        if isinstance(ip_addr, str):
            ip_addr = IPv4Address(ip_addr)
        if isinstance(network_addr, str):
            network_addr = IPv4Network(network_addr)
        ip_interface = IPv4Interface(f"{ip_addr}/{network_addr.prefixlen}")
        return Ip4Host(ip_addr, network_addr, ip_interface)

    @staticmethod
    def from_address_with_prefix(ip_with_prefix: str) -> Ip4Host:
        ip_intf = IPv4Interface(ip_with_prefix)
        return Ip4Host(ip_intf.ip, ip_intf.network, ip_intf)
